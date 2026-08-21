from core.pipeline.pipeline_context import PipelineContext
from core.pipeline.repair_pipeline import RepairPipeline


class DummyExecutionLoop:
    def process_error(self, error, retry_count):
        return {
            "error": error,
            "retry_count": retry_count,
        }


class DummyHealing:
    def __init__(self):
        self.execution_loop = DummyExecutionLoop()


class DummyCoder:
    def __init__(self, path):
        self.path = path

    def repair_code(self, recovery, implementation):
        return {
            "implementation_spec": {
                "files": [
                    {
                        "path": self.path,
                        "content": "print('fixed')",
                    }
                ]
            }
        }


class RecordingFilesystem:
    def __init__(self):
        self.calls = []

    def execute(self, *args):
        self.calls.append(args)

        return True


def test_repair_pipeline_writes_absolute_file_path_directly():
    filesystem = RecordingFilesystem()
    pipeline = RepairPipeline(
        DummyHealing(),
        DummyCoder("D:\\Jarvis\\Calculator\\src\\main.py"),
        filesystem,
    )
    context = PipelineContext(
        command="repair",
        target_project="D:\\Jarvis",
        generated_project="D:\\Jarvis",
        shared_context={},
    )

    pipeline.execute(
        context=context,
        implementation={},
        error="boom",
        retry_count=0,
    )

    assert filesystem.calls[0][1] == "D:\\Jarvis\\Calculator\\src\\main.py"


def test_repair_pipeline_resolves_relative_file_path_under_project_root():
    filesystem = RecordingFilesystem()
    pipeline = RepairPipeline(
        DummyHealing(),
        DummyCoder("Calculator\\src\\main.py"),
        filesystem,
    )
    context = PipelineContext(
        command="repair",
        target_project="D:\\Jarvis",
        generated_project="D:\\Jarvis",
        shared_context={},
    )

    pipeline.execute(
        context=context,
        implementation={},
        error="boom",
        retry_count=0,
    )

    assert filesystem.calls[0][1] == "D:\\Jarvis\\Calculator\\src\\main.py"
