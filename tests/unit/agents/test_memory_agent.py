"""
File: tests/unit/agents/test_memory_agent.py

Purpose:
Unit tests for MemoryAgent.

Why:
Verify memory documentation generation,
provider response handling, and
memory integration.
"""

from core.agents.memory_agent import (
    MemoryAgent
)


class StubProviderManager:
    def __init__(
        self,
        responses
    ):
        self.responses = responses
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

        # Pop the first response.
        return self.responses.pop(0)


def make_agent(
    responses
) -> MemoryAgent:
    agent = MemoryAgent()
    agent.provider_manager = StubProviderManager(
        responses
    )

    return agent


def test_memory_agent_creation():
    """
    Verify memory agent initialization.
    """

    agent = MemoryAgent()

    assert agent is not None


def test_generate_all_returns_expected_structure():
    """
    Verify generate_all returns the expected
    dictionary structure with all four files.
    """

    responses = [
        "# Architecture\n\n## Project Overview\n\nTest",
        "# Roadmap\n\n## Current Status\n\nTest",
        "# Project Context\n\n## Goal\n\nTest",
        "# Project Memory\n\n## Project Type\n\nTest",
    ]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    assert result["status"] == "generated"

    memory_files = result["memory_files"]

    assert "architecture.md" in memory_files
    assert "roadmap.md" in memory_files
    assert "project_context.md" in memory_files
    assert "memory.md" in memory_files


def test_plain_text_provider_responses_are_preserved():
    """
    Verify plain text provider responses
    are preserved as-is.
    """

    responses = [
        "# Architecture\n\nContent A",
        "# Roadmap\n\nContent B",
        "# Project Context\n\nContent C",
        "# Project Memory\n\nContent D",
    ]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    memory_files = result["memory_files"]

    assert (
        memory_files["architecture.md"]
        == "# Architecture\n\nContent A"
    )

    assert (
        memory_files["roadmap.md"]
        == "# Roadmap\n\nContent B"
    )

    assert (
        memory_files["project_context.md"]
        == "# Project Context\n\nContent C"
    )

    assert (
        memory_files["memory.md"]
        == "# Project Memory\n\nContent D"
    )


def test_parsed_dict_provider_response_is_converted_to_text():
    """
    Verify provider-layer parsed dict responses
    are converted to text (not kept as dict).
    """

    responses = [
        {"content": "# Architecture\n\nFrom Dict"},
        {"markdown": "# Roadmap\n\nFrom Dict"},
        {"documentation": "# Project Context\n\nFrom Dict"},
        {"generated_content": "# Project Memory\n\nFrom Dict"},
    ]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    memory_files = result["memory_files"]

    # All should be strings, not dicts.
    assert isinstance(
        memory_files["architecture.md"], str
    )

    assert isinstance(
        memory_files["roadmap.md"], str
    )

    assert isinstance(
        memory_files["project_context.md"], str
    )

    assert isinstance(
        memory_files["memory.md"], str
    )

    # Content should be extracted from the dict.
    assert (
        memory_files["architecture.md"]
        == "# Architecture\n\nFrom Dict"
    )

    assert (
        memory_files["roadmap.md"]
        == "# Roadmap\n\nFrom Dict"
    )

    assert (
        memory_files["project_context.md"]
        == "# Project Context\n\nFrom Dict"
    )

    assert (
        memory_files["memory.md"]
        == "# Project Memory\n\nFrom Dict"
    )


def test_parsed_list_provider_response_is_converted_to_text():
    """
    Verify provider-layer parsed list responses
    are converted to text.
    """

    responses = [
        ["# Architecture", "Line 2", "Line 3"],
        ["# Roadmap", "Line 2"],
        ["# Project Context", "Line 2"],
        ["# Project Memory", "Line 2"],
    ]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    memory_files = result["memory_files"]

    # All should be strings joined by newlines.
    assert isinstance(
        memory_files["architecture.md"], str
    )

    assert (
        memory_files["architecture.md"]
        == "# Architecture\nLine 2\nLine 3"
    )

    assert (
        memory_files["roadmap.md"]
        == "# Roadmap\nLine 2"
    )


def test_provider_called_for_each_documentation_task():
    """
    Verify provider is called four times with
    task_type="documentation".
    """

    responses = [
        "# Architecture",
        "# Roadmap",
        "# Project Context",
        "# Project Memory",
    ]

    agent = make_agent(responses[:])

    agent.generate_all(
        {"project_name": "test"}
    )

    assert len(agent.provider_manager.calls) == 4

    for call in agent.provider_manager.calls:
        assert call["task_type"] == "documentation"


def test_memory_stores_latest_architecture():
    """
    Verify the latest architecture is stored
    in agent memory.
    """

    responses = [
        "# Architecture",
        "# Roadmap",
        "# Project Context",
        "# Project Memory",
    ]

    agent = make_agent(responses[:])

    architecture = {"project_name": "test_app"}

    agent.generate_all(architecture)

    stored = agent.memory.retrieve("latest_architecture")

    assert stored == architecture


def test_provider_response_with_none_returns_empty_string():
    """
    Verify None response is handled gracefully.
    """

    responses = [None, None, None, None]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    # All should be empty strings.
    for content in result["memory_files"].values():
        assert content == ""


def test_provider_response_dict_without_content_keys_stringifies():
    """
    Verify dict without known content keys
    falls back to string representation.
    """

    responses = [
        {"unknown_key": "value"},
        {"another": "dict"},
        {"third": "item"},
        {"fourth": "entry"},
    ]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    expected_fragments = [
        "unknown_key",
        "another",
        "third",
        "fourth",
    ]

    # All should be strings (dict stringified).
    for content, expected_fragment in zip(
        result["memory_files"].values(),
        expected_fragments,
    ):
        assert isinstance(content, str)
        assert expected_fragment in content


def test_provider_response_dict_with_list_value():
    """
    Verify dict with list value for content key
    joins the list items.
    """

    responses = [
        {"content": ["Line 1", "Line 2"]},
        {"markdown": ["Item A", "Item B"]},
        {"documentation": ["First", "Second"]},
        {"generated_content": ["X", "Y", "Z"]},
    ]

    agent = make_agent(responses[:])

    result = agent.generate_all(
        {"project_name": "test"}
    )

    assert (
        result["memory_files"]["architecture.md"]
        == "Line 1\nLine 2"
    )

    assert (
        result["memory_files"]["roadmap.md"]
        == "Item A\nItem B"
    )

    assert (
        result["memory_files"]["project_context.md"]
        == "First\nSecond"
    )

    assert (
        result["memory_files"]["memory.md"]
        == "X\nY\nZ"
    )


def test_audit_event_created():
    """
    Verify audit event is logged.
    """

    responses = [
        "# Architecture",
        "# Roadmap",
        "# Project Context",
        "# Project Memory",
    ]

    agent = make_agent(responses[:])

    agent.generate_all(
        {"project_name": "test"}
    )

    # Should have at least one audit event.
    assert agent.audit_logger.count() >= 1
