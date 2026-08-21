from pathlib import Path

from core.pipeline.generation_pipeline import GenerationPipeline
from core.pipeline.software_engine import SoftwareEngine


class DummyRuntime:
    def __init__(self, active_project: str | None = None):
        self.active_project = active_project

    def get_active_project(self):
        return self.active_project


def test_generation_output_path_keeps_absolute_file_path():
    pipeline = GenerationPipeline(None, None, None)

    result = pipeline._output_path(
        "E:\\KAIROS\\.kairos\\generated",
        "D:\\Jarvis\\Calculator\\src\\main.py",
    )

    assert result == "D:\\Jarvis\\Calculator\\src\\main.py"


def test_generation_output_path_roots_relative_file_path_under_generated_project():
    pipeline = GenerationPipeline(None, None, None)

    result = pipeline._output_path(
        "E:\\KAIROS\\.kairos\\generated",
        "calculator/src/main.py",
    )

    assert result == str(
        Path("E:\\KAIROS\\.kairos\\generated")
        / "calculator/src/main.py"
    )


def test_software_engine_uses_absolute_target_project_directly():
    engine = object.__new__(SoftwareEngine)
    engine.generated_workspace = None
    engine.runtime = DummyRuntime("E:\\KAIROS")

    result = engine._resolve_generated_workspace("D:\\Jarvis")

    assert result == "D:\\Jarvis"


def test_software_engine_uses_generated_workspace_for_relative_project():
    engine = object.__new__(SoftwareEngine)
    engine.generated_workspace = None
    engine.runtime = DummyRuntime("E:\\KAIROS")

    result = engine._resolve_generated_workspace("calculator")

    assert result == str(
        Path("E:\\KAIROS")
        / ".kairos"
        / "generated"
    )
