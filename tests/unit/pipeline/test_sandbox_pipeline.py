import json

from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.sandbox_pipeline import SandboxPipeline


class RecordingFilesystem:
    def __init__(self):
        self.calls = []

    def execute(self, *args):
        self.calls.append(args)

        return True

    @property
    def sandbox_report(self):
        for action, path, content in self.calls:
            if action == "write" and path.endswith(".kairos\\sandbox.json"):
                return json.loads(content)

        raise AssertionError("sandbox.json was not written")


def test_sandbox_pipeline_runs_python_project_in_isolated_copy(tmp_path):
    project = tmp_path / "project"
    src = project / "src"
    src.mkdir(parents=True)
    (src / "main.py").write_text(
        "from pathlib import Path\n"
        "Path('sandbox_only.txt').write_text('created in sandbox')\n"
        "print('hello sandbox')\n",
        encoding="utf-8",
    )
    filesystem = RecordingFilesystem()
    pipeline = SandboxPipeline(filesystem)
    context = PipelineContext(
        command="run",
        target_project=str(project),
        generated_project=str(project),
        shared_context={},
    )

    result = pipeline.execute(
        context=context,
        architecture={
            "entry_point": "src/main.py",
        },
        implementation={},
    )

    report = filesystem.sandbox_report
    assert result.success is True
    assert report["status"] == "success"
    assert report["runtime"] == "python"
    assert report["exit_code"] == 0
    assert "hello sandbox" in report["logs"]["stdout"]
    assert not (project / "sandbox_only.txt").exists()


def test_sandbox_pipeline_reports_python_runtime_failure(tmp_path):
    project = tmp_path / "project"
    src = project / "src"
    src.mkdir(parents=True)
    (src / "main.py").write_text(
        "raise RuntimeError('boom')\n",
        encoding="utf-8",
    )
    filesystem = RecordingFilesystem()
    pipeline = SandboxPipeline(filesystem)
    context = PipelineContext(
        command="run",
        target_project=str(project),
        generated_project=str(project),
        shared_context={},
    )

    result = pipeline.execute(
        context=context,
        architecture={
            "entry_point": "src/main.py",
        },
        implementation={},
    )

    report = filesystem.sandbox_report
    assert result.success is False
    assert report["status"] == "failed"
    assert report["exit_code"] != 0
    assert "RuntimeError" in report["logs"]["stderr"]
    assert "runtime exception" in report["errors"]
