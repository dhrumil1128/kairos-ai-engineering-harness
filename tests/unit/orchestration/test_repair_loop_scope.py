import pytest
from unittest.mock import MagicMock
from core.orchestration.repair_loop import RepairLoop

@pytest.fixture
def sample_implementation():
    return {
        "status": "generated",
        "implementation_spec": {
            "files": [
                {"path": "src/main.py", "content": "print('hello')"},
                {"path": "docs/README.md", "content": "# Readme"},
                {"path": "requirements.txt", "content": "click"},
            ]
        }
    }

def test_case_1_only_readme(sample_implementation):
    coordinator = MagicMock()
    coordinator.repair.return_value = {
        "success": True,
        "message": "Repaired",
        "implementation": {
            "implementation_spec": {
                "files": [
                    {"path": "docs/README.md", "content": "# Updated Readme"}
                ]
            }
        },
        "review": {"approved": True},
        "agent_context": MagicMock()
    }
    
    config = MagicMock()
    config.max_retries = 1
    
    repair_loop = RepairLoop(coordinator=coordinator, config=config)
    review = {"generated_review": "Documentation issue in docs/README.md missing section"}
    
    result = repair_loop.run(
        agent_context=MagicMock(),
        implementation=sample_implementation,
        review=review,
    )
    
    # Check that coordinator.repair received ONLY docs/README.md in target implementation
    called_impl = coordinator.repair.call_args.kwargs["implementation"]
    called_files = [f["path"] for f in called_impl["implementation_spec"]["files"]]
    assert called_files == ["docs/README.md"]
    
    # Check merged output contains updated README and untouched main.py & requirements.txt
    merged_files = {f["path"]: f["content"] for f in result["implementation"]["implementation_spec"]["files"]}
    assert merged_files["docs/README.md"] == "# Updated Readme"
    assert merged_files["src/main.py"] == "print('hello')"
    assert merged_files["requirements.txt"] == "click"

def test_case_2_only_main_py(sample_implementation):
    coordinator = MagicMock()
    coordinator.repair.return_value = {
        "success": True,
        "message": "Repaired",
        "implementation": {
            "implementation_spec": {
                "files": [
                    {"path": "src/main.py", "content": "print('fixed main')"}
                ]
            }
        },
        "review": {"approved": True},
        "agent_context": MagicMock()
    }
    
    config = MagicMock()
    config.max_retries = 1
    
    repair_loop = RepairLoop(coordinator=coordinator, config=config)
    review = {"generated_review": "Syntax error in src/main.py line 2"}
    
    result = repair_loop.run(
        agent_context=MagicMock(),
        implementation=sample_implementation,
        review=review,
    )
    
    called_impl = coordinator.repair.call_args.kwargs["implementation"]
    called_files = [f["path"] for f in called_impl["implementation_spec"]["files"]]
    assert called_files == ["src/main.py"]
    
    merged_files = {f["path"]: f["content"] for f in result["implementation"]["implementation_spec"]["files"]}
    assert merged_files["src/main.py"] == "print('fixed main')"
    assert merged_files["docs/README.md"] == "# Readme"

def test_case_3_readme_and_requirements(sample_implementation):
    coordinator = MagicMock()
    coordinator.repair.return_value = {
        "success": True,
        "message": "Repaired",
        "implementation": {
            "implementation_spec": {
                "files": [
                    {"path": "docs/README.md", "content": "# Fixed Readme"},
                    {"path": "requirements.txt", "content": "click\npytest"}
                ]
            }
        },
        "review": {"approved": True},
        "agent_context": MagicMock()
    }
    
    config = MagicMock()
    config.max_retries = 1
    
    repair_loop = RepairLoop(coordinator=coordinator, config=config)
    review = {"generated_review": "Please update README.md and requirements.txt with pytest"}
    
    result = repair_loop.run(
        agent_context=MagicMock(),
        implementation=sample_implementation,
        review=review,
    )
    
    called_impl = coordinator.repair.call_args.kwargs["implementation"]
    called_files = set(f["path"] for f in called_impl["implementation_spec"]["files"])
    assert called_files == {"docs/README.md", "requirements.txt"}
    
    merged_files = {f["path"]: f["content"] for f in result["implementation"]["implementation_spec"]["files"]}
    assert merged_files["docs/README.md"] == "# Fixed Readme"
    assert merged_files["requirements.txt"] == "click\npytest"
    assert merged_files["src/main.py"] == "print('hello')"

def test_case_4_no_filenames_specified(sample_implementation):
    coordinator = MagicMock()
    coordinator.repair.return_value = {
        "success": True,
        "message": "Repaired",
        "implementation": sample_implementation,
        "review": {"approved": True},
        "agent_context": MagicMock()
    }
    
    config = MagicMock()
    config.max_retries = 1
    
    repair_loop = RepairLoop(coordinator=coordinator, config=config)
    review = {"generated_review": "Overall code quality is insufficient."}
    
    result = repair_loop.run(
        agent_context=MagicMock(),
        implementation=sample_implementation,
        review=review,
    )
    
    called_impl = coordinator.repair.call_args.kwargs["implementation"]
    called_files = [f["path"] for f in called_impl["implementation_spec"]["files"]]
    # Full implementation passed when no filenames identified
    assert set(called_files) == {"src/main.py", "docs/README.md", "requirements.txt"}
