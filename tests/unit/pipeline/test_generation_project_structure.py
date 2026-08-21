from core.pipeline.generation_pipeline import GenerationPipeline
from core.pipeline.pipeline_context import PipelineContext


class DummyMemoryAgent:
    def generate_all(self, architecture):
        return {
            "status": "generated",
            "memory_files": {
                "architecture.md": "# Architecture",
                "roadmap.md": "# Roadmap",
                "project_context.md": "# Project Context",
                "memory.md": "# Memory",
            },
        }


class DummyCoder:
    def generate_code(self, architecture, context=None):
        return {
            "status": "generated",
            "implementation_spec": {
                "files": [
                    {
                        "path": "src/main.py",
                        "content": "from calculator import add\n\nprint(add(1, 2))",
                    },
                    {
                        "path": "calculator/src/main/python/calculator.py",
                        "content": "def add(left, right):\n    return left + right\n",
                    },
                    {
                        "path": "docs/README.md",
                        "content": "# Calculator",
                    },
                    {
                        "path": "tests/test_main.py",
                        "content": "from calculator import add\n\n\ndef test_add():\n    assert add(1, 2) == 3\n",
                    },
                    {
                        "path": "architecture.md",
                        "content": "# Old Location",
                    },
                    {
                        "path": ".kairos/generated_code.py",
                        "content": "print('bad')",
                    },
                ]
            },
        }


class RecordingFilesystem:
    def __init__(self):
        self.calls = []

    def execute(self, *args):
        self.calls.append(args)

        return True


def test_generation_pipeline_writes_production_project_structure():
    filesystem = RecordingFilesystem()
    pipeline = GenerationPipeline(
        DummyMemoryAgent(),
        DummyCoder(),
        filesystem,
    )
    context = PipelineContext(
        command="build calculator",
        target_project="D:\\Jarvis\\Calculator",
        generated_project="D:\\Jarvis\\Calculator",
        shared_context={},
    )
    architecture = {
        "project_name": "Calculator",
        "project_type": "python application",
        "entry_point": "src/main.py",
        "package_name": "calculator",
        "requirements": ["pytest", "pytest"],
        "directories": ["src", "src", "docs", "empty"],
    }

    result = pipeline.execute(context, architecture)
    write_paths = [
        call[1]
        for call in filesystem.calls
        if call[0] == "write"
    ]

    assert result.success is True
    assert "D:\\Jarvis\\Calculator\\README.md" in write_paths
    assert "D:\\Jarvis\\Calculator\\requirements.txt" in write_paths
    assert "D:\\Jarvis\\Calculator\\.gitignore" in write_paths
    assert "D:\\Jarvis\\Calculator\\src\\main.py" in write_paths
    assert "D:\\Jarvis\\Calculator\\calculator\\__init__.py" in write_paths
    assert "D:\\Jarvis\\Calculator\\calculator\\calculator.py" in write_paths
    assert "D:\\Jarvis\\Calculator\\docs\\architecture.md" in write_paths
    assert "D:\\Jarvis\\Calculator\\docs\\roadmap.md" in write_paths
    assert "D:\\Jarvis\\Calculator\\docs\\project_context.md" in write_paths
    assert "D:\\Jarvis\\Calculator\\docs\\memory.md" in write_paths
    assert "D:\\Jarvis\\Calculator\\.kairos\\pipeline.json" in write_paths
    assert "D:\\Jarvis\\Calculator\\.kairos\\cache\\manifest.json" in write_paths
    assert "D:\\Jarvis\\Calculator\\.kairos\\logs\\generation.json" in write_paths
    assert "D:\\Jarvis\\Calculator\\.kairos\\architecture.md" not in write_paths
    assert "D:\\Jarvis\\Calculator\\.kairos\\generated_code.py" not in write_paths
    assert not any(call[0] == "create_directory" for call in filesystem.calls)

    implementation_paths = [
        file["path"]
        for file in result.data["implementation"]["implementation_spec"]["files"]
    ]

    assert not any(path.startswith(".kairos/") for path in implementation_paths)
    assert "src/main.py" in implementation_paths
    assert "calculator/__init__.py" in implementation_paths
    assert "calculator/calculator.py" in implementation_paths
    assert "calculator/src/main/python/calculator.py" not in implementation_paths


class MissingImportCoder:
    def generate_code(self, architecture, context=None):
        return {
            "status": "generated",
            "implementation_spec": {
                "files": [
                    {
                        "path": "src/main.py",
                        "content": "import missing_package\n\nprint('bad')",
                    },
                    {
                        "path": "calculator/calculator.py",
                        "content": "def add(left, right):\n    return left + right\n",
                    },
                    {
                        "path": "tests/test_main.py",
                        "content": "def test_placeholder():\n    assert True\n",
                    },
                    {
                        "path": "docs/README.md",
                        "content": "# Calculator\n",
                    },
                ]
            },
        }


def test_generation_pipeline_fails_before_write_when_import_has_no_module():
    filesystem = RecordingFilesystem()
    pipeline = GenerationPipeline(
        DummyMemoryAgent(),
        MissingImportCoder(),
        filesystem,
    )
    context = PipelineContext(
        command="build calculator",
        target_project="D:\\Jarvis\\Calculator",
        generated_project="D:\\Jarvis\\Calculator",
        shared_context={},
    )
    architecture = {
        "project_name": "Calculator",
        "project_type": "python application",
        "entry_point": "src/main.py",
        "package_name": "calculator",
        "requirements": [],
        "directories": ["src", "calculator", "tests", "docs"],
        "files": [
            "src/main.py",
            "calculator/calculator.py",
        ],
    }

    try:
        pipeline.execute(context, architecture)
    except ValueError as error:
        assert "missing_package" in str(error)
    else:
        raise AssertionError("Generation should fail for unresolved imports")

    assert filesystem.calls == []


class FlaskImportCoder:
    def generate_code(self, architecture, context=None):
        return {
            "status": "generated",
            "implementation_spec": {
                "files": [
                    {
                        "path": "src/main.py",
                        "content": "from student_api.student_api import create_app\n\napp = create_app()\n",
                    },
                    {
                        "path": "student_api/student_api.py",
                        "content": "from flask import Flask\n\n\ndef create_app():\n    return Flask(__name__)\n",
                    },
                    {
                        "path": "tests/test_main.py",
                        "content": "from student_api.student_api import create_app\n\n\ndef test_create_app():\n    assert create_app() is not None\n",
                    },
                    {
                        "path": "docs/README.md",
                        "content": "# Student API\n",
                    },
                ]
            },
        }


def test_generation_pipeline_matches_dependency_import_case_insensitively():
    filesystem = RecordingFilesystem()
    pipeline = GenerationPipeline(
        DummyMemoryAgent(),
        FlaskImportCoder(),
        filesystem,
    )
    context = PipelineContext(
        command="build flask api",
        target_project="D:\\Projects\\StudentAPI",
        generated_project="D:\\Projects\\StudentAPI",
        shared_context={},
    )
    architecture = {
        "project_name": "StudentAPI",
        "project_type": "Flask REST API",
        "framework": "Flask",
        "entry_point": "src/main.py",
        "package_name": "student_api",
        "requirements": ["Flask", "Flask-SQLAlchemy"],
        "directories": ["src", "student_api", "tests", "docs"],
        "files": [
            "src/main.py",
            "student_api/__init__.py",
            "student_api/student_api.py",
            "tests/test_main.py",
            "docs/README.md",
        ],
    }

    result = pipeline.execute(context, architecture)

    assert result.success is True


class DynamicSymbolCoder:
    def generate_code(self, architecture, context=None):
        return {
            "status": "generated",
            "implementation_spec": {
                "files": [
                    {
                        "path": "src/main.py",
                        "content": "from student_api.routes import main\n\napp = main\n",
                    },
                    {
                        "path": "student_api/student_api.py",
                        "content": "def create_app():\n    return None\n",
                    },
                    {
                        "path": "student_api/routes.py",
                        "content": "def create_blueprint():\n    return None\n",
                    },
                    {
                        "path": "tests/test_main.py",
                        "content": "def test_placeholder():\n    assert True\n",
                    },
                    {
                        "path": "docs/README.md",
                        "content": "# Student API\n",
                    },
                ]
            },
        }


def test_generation_pipeline_allows_existing_module_with_dynamic_symbol():
    filesystem = RecordingFilesystem()
    pipeline = GenerationPipeline(
        DummyMemoryAgent(),
        DynamicSymbolCoder(),
        filesystem,
    )
    context = PipelineContext(
        command="build flask api",
        target_project="D:\\Projects\\StudentAPI",
        generated_project="D:\\Projects\\StudentAPI",
        shared_context={},
    )
    architecture = {
        "project_name": "StudentAPI",
        "project_type": "Flask REST API",
        "framework": "Flask",
        "entry_point": "src/main.py",
        "package_name": "student_api",
        "requirements": ["Flask"],
        "directories": ["src", "student_api", "tests", "docs"],
        "files": [
            "src/main.py",
            "student_api/__init__.py",
            "student_api/student_api.py",
            "student_api/routes.py",
            "tests/test_main.py",
            "docs/README.md",
        ],
    }

    result = pipeline.execute(context, architecture)

    assert result.success is True
