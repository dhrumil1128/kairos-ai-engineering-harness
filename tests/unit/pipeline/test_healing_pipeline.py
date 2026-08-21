import json

from core.pipeline.healing_pipeline import HealingPipeline
from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.pipeline_result import PipelineResult


class DummyExecutionLoop:
    def process_error(self, error_message, attempt):
        return {
            "status": "retry",
            "analysis": {
                "error": error_message,
            },
            "repair_plan": {
                "action": "fix",
            },
            "attempt": attempt + 1,
        }


class DummyHealing:
    def __init__(self):
        self.execution_loop = DummyExecutionLoop()


class DummyCoder:
    def __init__(self):
        self.received_files = []
        self.provider_manager = DummyProvider(self)


class DummyProvider:
    def __init__(self, coder):
        self.coder = coder
        self.prompts = []
        self.response = "print('fixed')"

    def execute(self, task_type, prompt):
        self.prompts.append(prompt)

        if "src/main.py" in prompt:
            self.coder.received_files.append("src/main.py")

        if "src/other.py" in prompt:
            self.coder.received_files.append("src/other.py")

        return self.response


class PassingValidation:
    def execute(self, project_path, architecture, implementation):
        return {
            "passed": True,
            "summary": {},
            "report": {},
            "failed_validators": [],
        }


class RecordingSandbox:
    def __init__(self, success=True):
        self.success = success
        self.calls = 0

    def execute(self, context, architecture, implementation):
        self.calls += 1
        data = {
            "success": self.success,
            "status": "success" if self.success else "failed",
            "logs": {
                "stderr": "" if self.success else "RuntimeError: still broken",
            },
            "errors": [] if self.success else ["RuntimeError: still broken"],
        }

        if self.success:
            return PipelineResult.success_result(
                pipeline="sandbox",
                data=data,
            )

        return PipelineResult.failure_result(
            pipeline="sandbox",
            data=data,
        )


class RecordingFilesystem:
    def __init__(self):
        self.calls = []

    def execute(self, *args):
        self.calls.append(args)

        return True

    def written_json(self, filename):
        for call in self.calls:
            if call[0] == "write" and call[1].endswith(filename):
                return json.loads(call[2])

        raise AssertionError(f"{filename} was not written")


def _context():
    return PipelineContext(
        command="heal",
        target_project="D:\\Jarvis\\Calculator",
        generated_project="D:\\Jarvis\\Calculator",
        shared_context={},
    )


def _implementation():
    return {
        "implementation_spec": {
            "files": [
                {
                    "path": "src/main.py",
                    "content": "raise RuntimeError('boom')",
                },
                {
                    "path": "src/other.py",
                    "content": "print('untouched')",
                },
            ]
        }
    }


def test_healing_pipeline_writes_successful_noop_report():
    filesystem = RecordingFilesystem()
    pipeline = HealingPipeline(
        DummyHealing(),
        DummyCoder(),
        filesystem,
        validation_pipeline=PassingValidation(),
        sandbox_pipeline=RecordingSandbox(),
    )

    result = pipeline.execute(
        context=_context(),
        architecture={},
        implementation=_implementation(),
        sandbox_result=PipelineResult.success_result(
            pipeline="sandbox",
            data={
                "logs": {
                    "stderr": "",
                }
            },
        ),
    )

    report = filesystem.written_json("healing.json")
    assert result.success is True
    assert report["status"] == "success"
    assert report["detected_issues"] == []
    assert report["modified_files"] == []


def test_healing_pipeline_repairs_only_affected_files():
    filesystem = RecordingFilesystem()
    coder = DummyCoder()
    pipeline = HealingPipeline(
        DummyHealing(),
        coder,
        filesystem,
        validation_pipeline=PassingValidation(),
        sandbox_pipeline=RecordingSandbox(),
    )
    stderr = (
        'Traceback (most recent call last):\n'
        '  File "D:\\Jarvis\\Calculator\\src\\main.py", line 1, in <module>\n'
        "RuntimeError: boom\n"
    )

    result = pipeline.execute(
        context=_context(),
        architecture={},
        implementation=_implementation(),
        sandbox_result=PipelineResult.failure_result(
            pipeline="sandbox",
            data={
                "logs": {
                    "stderr": stderr,
                },
                "errors": [stderr],
            },
        ),
    )

    report = filesystem.written_json("healing.json")
    modified_source_paths = [
        call[1]
        for call in filesystem.calls
        if call[0] == "write" and call[1].endswith("src\\main.py")
    ]

    assert result.success is True
    assert coder.received_files == ["src/main.py"]
    assert "repair_plan" not in coder.provider_manager.prompts[0].lower()
    assert "repair plan" not in coder.provider_manager.prompts[0].lower()
    assert modified_source_paths == ["D:\\Jarvis\\Calculator\\src\\main.py"]
    assert report["status"] == "success"
    assert report["modified_files"] == ["src/main.py"]
    assert report["remaining_issues"] == []


def test_healing_pipeline_does_not_repeat_successful_repair():
    filesystem = RecordingFilesystem()
    coder = DummyCoder()
    pipeline = HealingPipeline(
        DummyHealing(),
        coder,
        filesystem,
        validation_pipeline=PassingValidation(),
        sandbox_pipeline=RecordingSandbox(),
    )

    result = pipeline.execute(
        context=_context(),
        architecture={},
        implementation=_implementation(),
        validation_result=PipelineResult.failure_result(
            pipeline="validation",
            data={
                "report": {
                    "syntax": {
                        "errors": ["SyntaxError: invalid syntax in src/main.py"],
                    }
                },
                "failed_validators": ["syntax"],
            },
        ),
        repair_result=PipelineResult.success_result(
            pipeline="repair",
            data={
                "implementation": _implementation(),
            },
        ),
        sandbox_result=PipelineResult.success_result(
            pipeline="sandbox",
            data={
                "logs": {
                    "stderr": "",
                }
            },
        ),
    )

    report = filesystem.written_json("healing.json")

    assert result.success is True
    assert coder.received_files == []
    assert report["detected_issues"] == []
    assert report["modified_files"] == []


def test_healing_pipeline_rejects_explanatory_file_content():
    filesystem = RecordingFilesystem()
    coder = DummyCoder()
    coder.provider_manager.response = "This code applies the repair plan by fixing it."
    pipeline = HealingPipeline(
        DummyHealing(),
        coder,
        filesystem,
        validation_pipeline=PassingValidation(),
        sandbox_pipeline=RecordingSandbox(),
    )
    stderr = (
        'Traceback (most recent call last):\n'
        '  File "D:\\Jarvis\\Calculator\\src\\main.py", line 1, in <module>\n'
        "RuntimeError: boom\n"
    )

    result = pipeline.execute(
        context=_context(),
        architecture={},
        implementation=_implementation(),
        sandbox_result=PipelineResult.failure_result(
            pipeline="sandbox",
            data={
                "logs": {
                    "stderr": stderr,
                },
                "errors": [stderr],
            },
        ),
    )

    source_writes = [
        call
        for call in filesystem.calls
        if call[0] == "write" and call[1].endswith("src\\main.py")
    ]

    assert result.success is False
    assert source_writes == []


def test_healing_pipeline_stops_when_sandbox_retry_fails():
    filesystem = RecordingFilesystem()
    sandbox = RecordingSandbox(success=False)
    pipeline = HealingPipeline(
        DummyHealing(),
        DummyCoder(),
        filesystem,
        validation_pipeline=PassingValidation(),
        sandbox_pipeline=sandbox,
        max_retries=1,
    )
    stderr = (
        'Traceback (most recent call last):\n'
        '  File "D:\\Jarvis\\Calculator\\src\\main.py", line 1, in <module>\n'
        "RuntimeError: boom\n"
    )

    result = pipeline.execute(
        context=_context(),
        architecture={},
        implementation=_implementation(),
        sandbox_result=PipelineResult.failure_result(
            pipeline="sandbox",
            data={
                "logs": {
                    "stderr": stderr,
                },
                "errors": [stderr],
            },
        ),
    )

    assert result.success is False
    assert sandbox.calls == 1
