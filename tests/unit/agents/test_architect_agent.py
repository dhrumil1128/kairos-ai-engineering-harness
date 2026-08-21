"""
File: tests/unit/agents/test_architect_agent.py

Purpose:
Unit tests for ArchitectAgent.
"""

from core.agents.architect_agent import (
    ArchitectAgent
)

from core.architecture.blueprint import (
    ArchitectureBlueprint
)


class StubProviderManager:
    def __init__(
        self,
        response: dict
    ):
        self.response = response
        self.calls = []

    def execute(
        self,
        task_type: str,
        prompt: str
    ):
        self.calls.append(
            {
                "task_type": task_type,
                "prompt": prompt,
            }
        )

        return self.response


def make_agent(
    response: dict | None = None
) -> ArchitectAgent:
    agent = ArchitectAgent()
    agent.provider_manager = StubProviderManager(
        response
        or {
            "project_name": "kairos_app",
            "project_type": "CLI application",
            "framework": "click",
            "language": "Python",
            "requirements": [],
        }
    )

    return agent


def make_plan() -> dict:
    return {
        "task": "Build a CLI calculator",
        "generated_plan": "Create commands, calculator logic, tests, and docs.",
    }


def test_architect_creation():
    """
    Verify architect initialization.
    """

    agent = ArchitectAgent()

    assert agent is not None


def test_create_architecture():
    """
    Verify architecture creation.
    """

    agent = make_agent()

    architecture = (
        agent.create_architecture(
            make_plan()
        )
    )

    assert isinstance(
        architecture,
        ArchitectureBlueprint
    )

    assert (
        architecture.project_name
        == "kairos_app"
    )


def test_blueprint_structure_exists():
    """
    Verify current deterministic blueprint structure.
    """

    agent = make_agent()

    architecture = (
        agent.create_architecture(
            make_plan()
        )
    )

    assert (
        "src/main.py"
        in architecture.files
    )

    assert (
        "tests"
        in architecture.directories
    )

    assert (
        "click"
        in architecture.requirements
    )


def test_plan_saved_to_memory():
    """
    Verify plan persistence.
    """

    agent = make_agent()

    plan = make_plan()

    agent.create_architecture(
        plan
    )

    stored = (
        agent.memory.retrieve(
            "latest_plan"
        )
    )

    assert stored == plan


def test_provider_called_for_architecture_task():
    """
    Verify the provider is called with the current task type.
    """

    agent = make_agent()

    agent.create_architecture(
        make_plan()
    )

    assert (
        agent.provider_manager.calls[0]["task_type"]
        == "architecture"
    )
    
def test_provider_manager_exists():

    agent = (
        ArchitectAgent()
    )

    assert hasattr(
        agent,
        "provider_manager"
    )


def test_parse_intent_response_accepts_parsed_dict():
    agent = ArchitectAgent()

    response = {
        "project_name": "kairos_app",
        "project_type": "cli",
        "framework": "",
        "language": "Python",
        "requirements": [],
    }

    assert agent._parse_intent_response(response) is response


def test_parse_intent_response_keeps_plain_text_fallback():
    agent = ArchitectAgent()

    response = """
```json
{
    "project_name": "kairos_app",
    "project_type": "cli",
    "framework": "",
    "language": "Python",
    "requirements": []
}
```
"""

    intent = agent._parse_intent_response(response)

    assert intent["project_name"] == "kairos_app"
    assert intent["requirements"] == []


def test_parse_intent_response_rejects_parsed_list():
    agent = ArchitectAgent()

    try:
        agent._parse_intent_response([])
    except ValueError as error:
        assert "JSON object" in str(error)
    else:
        raise AssertionError("Expected ValueError")


def test_flask_architecture_adds_framework_files():
    agent = make_agent(
        {
            "project_name": "student_api",
            "project_type": "Flask REST API",
            "framework": "Flask",
            "language": "Python",
            "requirements": [],
        }
    )

    architecture = agent.create_architecture(
        make_plan()
    )

    files = architecture.files

    assert "student_api/routes.py" in files
    assert "student_api/models.py" in files
    assert "student_api/services.py" in files
    assert "student_api/config.py" in files


def test_scenario_1_explicit_files_override_generic_template():
    """
    Scenario 1: User explicitly requests main.py and README.md with no folders.
    Expected: Generate only main.py and README.md.
    """
    agent = make_agent(
        {
            "project_name": "Calculator",
            "project_type": "Implementation",
            "framework": None,
            "language": "Python",
            "requirements": [],
        }
    )

    plan = {
        "task": """Create a Python calculator.

Files:
- main.py
- README.md

Generate ONLY these two files.
Do NOT create folders.
Do NOT create tests.
Do NOT create extra files."""
    }

    architecture = agent.create_architecture(plan)

    assert architecture.files == ["main.py", "README.md"]
    assert architecture.directories == []
    assert architecture.entry_point == "main.py"


def test_scenario_2_flask_without_explicit_files_uses_template():
    """
    Scenario 2: User requests Flask API without specifying files.
    Expected: Flask Framework Template is used.
    """
    agent = make_agent(
        {
            "project_name": "student_api",
            "project_type": "Flask REST API",
            "framework": "Flask",
            "language": "Python",
            "requirements": [],
        }
    )

    plan = {"task": "Create a Flask REST API for student management."}

    architecture = agent.create_architecture(plan)

    assert "student_api/routes.py" in architecture.files
    assert "student_api/models.py" in architecture.files


def test_scenario_3_generic_python_without_explicit_files_uses_generic_template():
    """
    Scenario 3: User requests generic Python project without specifying files.
    Expected: Generic Python Template is used.
    """
    agent = make_agent(
        {
            "project_name": "calculator_app",
            "project_type": "CLI Application",
            "framework": None,
            "language": "Python",
            "requirements": [],
        }
    )

    plan = {"task": "Build a generic CLI calculator."}

    architecture = agent.create_architecture(plan)

    assert "src/main.py" in architecture.files
    assert "tests" in architecture.directories


def test_scenario_4_custom_folder_structure_respected_exactly():
    """
    Scenario 4: User specifies a custom folder structure.
    Expected: Respect custom structure exactly.
    """
    agent = make_agent(
        {
            "project_name": "custom_app",
            "project_type": "Script",
            "framework": None,
            "language": "Python",
            "requirements": [],
        }
    )

    plan = {
        "task": """Create a custom tool.

Files:
- bin/app.py
- config/settings.json
- docs/index.md"""
    }

    architecture = agent.create_architecture(plan)

    assert architecture.files == ["bin/app.py", "config/settings.json", "docs/index.md"]
    assert set(architecture.directories) == {"bin", "config", "docs"}
    assert architecture.entry_point == "bin/app.py"

