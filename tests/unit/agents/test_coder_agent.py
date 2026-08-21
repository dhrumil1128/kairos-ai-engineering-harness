"""
File:
tests/unit/agents/
test_coder_agent.py

Purpose:
Verify coder agent.
"""

from core.agents.coder_agent import (
    CoderAgent
)

from core.architecture.blueprint import (
    ArchitectureBlueprint
)


class StubProviderManager:
    def __init__(
        self,
        responses
    ):
        if isinstance(responses, tuple):
            self.responses = list(responses)
        else:
            self.responses = [responses]

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

        if len(self.responses) > 1:
            return self.responses.pop(0)

        return self.responses[0]


def make_architecture(
    files: list[str] | None = None
) -> ArchitectureBlueprint:
    return ArchitectureBlueprint(
        project_name="kairos_app",
        project_type="CLI application",
        framework="",
        language="Python",
        package_name="kairos_app",
        entry_point="src/main.py",
        entry_module="main.py",
        entry_function="main",
        directories=[
            "src",
            "tests",
        ],
        files=files or [
            "src/main.py",
        ],
        requirements=[],
        framework_template="generic_python",
        code_style="standard",
    )


def make_agent(
    responses="print('hello')"
) -> CoderAgent:
    agent = CoderAgent()
    agent.provider_manager = StubProviderManager(
        responses
    )

    return agent


def generated_file_content(
    result: dict,
    path: str
) -> str:
    for file in result["implementation_spec"]["files"]:
        if file["path"] == path:
            return file["content"]

    raise AssertionError(
        f"Generated file not found: {path}"
    )


def test_agent_creation():
    """
    Verify creation.
    """

    agent = CoderAgent()

    assert agent is not None


def test_generate_code_returns_dict():

    agent = make_agent()

    result = agent.generate_code(
        make_architecture()
    )

    assert isinstance(
        result,
        dict
    )


def test_files_generated():
    """
    Verify current implementation spec file generation.
    """

    agent = make_agent(
        "print('hello')"
    )

    result = agent.generate_code(
        make_architecture()
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == "print('hello')"


def test_provider_manager_exists():

    agent = (
        CoderAgent()
    )

    assert hasattr(
        agent,
        "provider_manager"
    )


def test_generate_code_status():

    agent = make_agent()

    result = agent.generate_code(
        make_architecture()
    )

    assert (
        result["status"]
        == "generated"
    )


def test_generated_implementation_saved_to_memory():

    agent = make_agent()

    result = agent.generate_code(
        make_architecture()
    )

    assert (
        agent.memory.retrieve(
            "latest_implementation"
        )
        == result
    )


def test_plain_text_provider_response_is_supported():
    """
    Verify plain text responses keep the existing cleanup behavior.
    """

    agent = make_agent(
        "```python\nprint('hello')\n```"
    )

    result = agent.generate_code(
        make_architecture()
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == "print('hello')"


def test_parsed_dict_provider_response_is_supported():
    """
    Verify provider-layer parsed dict responses can supply file content.
    """

    agent = make_agent(
        {
            "content": "print('from dict')"
        }
    )

    result = agent.generate_code(
        make_architecture()
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == "print('from dict')"


def test_parsed_list_provider_response_is_supported():
    """
    Verify provider-layer parsed list responses can supply file content.
    """

    agent = make_agent(
        [
            "def main():",
            "    print('from list')",
        ]
    )

    result = agent.generate_code(
        make_architecture()
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == "def main():\n    print('from list')"


def test_structured_file_list_selects_current_file():
    """
    Verify multi-file structured responses use the requested file.
    """

    agent = make_agent(
        {
            "files": [
                {
                    "path": "other.py",
                    "content": "print('wrong')",
                },
                {
                    "path": "src/main.py",
                    "content": "print('right')",
                },
            ]
        }
    )

    result = agent.generate_code(
        make_architecture()
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == "print('right')"


def test_provider_called_for_coding_task():
    """
    Verify provider execution behavior is unchanged.
    """

    agent = make_agent()

    agent.generate_code(
        make_architecture()
    )

    assert (
        agent.provider_manager.calls[0]["task_type"]
        == "coding"
    )


def test_explicit_user_code_bypasses_provider_and_is_preserved():
    """
    Verify user-supplied file source is treated as the implementation.
    """

    explicit_code = (
        "def greet():\n"
        "    print(\"Hello from KAIROS!\")\n"
        "\n"
        "if __name__ == \"__main__\":\n"
        "    greet()"
    )
    architecture = make_architecture()
    architecture.metadata["user_request"] = (
        "Create src/main.py with this code:\n\n"
        f"{explicit_code}"
    )

    agent = make_agent(
        "def greet() -> str:\n"
        "    return \"Hello from KAIROS!\""
    )

    result = agent.generate_code(
        architecture
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == explicit_code
    assert agent.provider_manager.calls == []


def test_invalid_explicit_user_code_falls_back_to_provider():
    """
    Verify syntactically invalid inline source can still be generated.
    """

    architecture = make_architecture()
    architecture.metadata["user_request"] = (
        "Create src/main.py with this code:\n\n"
        "def greet(:\n"
        "    print(\"broken\")"
    )

    agent = make_agent(
        "print('generated fallback')"
    )

    result = agent.generate_code(
        architecture
    )

    assert generated_file_content(
        result,
        "src/main.py"
    ) == "print('generated fallback')"
    assert len(agent.provider_manager.calls) == 1
