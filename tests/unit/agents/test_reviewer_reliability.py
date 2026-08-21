import pytest
from core.agents.reviewer_agent import ReviewerAgent

@pytest.fixture
def reviewer():
    return ReviewerAgent()

def test_case_1_valid_calculator_project_approved(reviewer):
    response = """
    **Review Summary:**
    The implementation is well-structured and implements all requested operations.
    
    Overall Status: Accepted
    """
    assert reviewer._is_approved_response(response) is True

def test_case_2_readme_missing_installation_medium_severity(reviewer):
    response = """
    **Issues Found:**
    1. Documentation Issue
       - File: docs/README.md
       - Evidence: Installation section is absent from README.md.
       - Severity: Medium
       - Recommendation: Add installation steps.
    
    Overall Status: Accepted with Minor Improvements
    """
    assert reviewer._is_approved_response(response) is True

def test_case_3_python_syntax_error_critical_severity(reviewer):
    response = """
    **Issues Found:**
    1. Syntax Error
       - File: src/main.py
       - Evidence: Line 10: `def main(:` causes SyntaxError
       - Severity: Critical
       - Recommendation: Fix function declaration.
    
    Overall Status: Changes Requested
    """
    assert reviewer._is_approved_response(response) is False

def test_case_4_style_suggestions_only_low_severity(reviewer):
    response = """
    **Issues Found:**
    1. Code Style
       - File: src/main.py
       - Evidence: Variable name `x` should be more descriptive.
       - Severity: Low
       - Recommendation: Rename `x` to `result`.
    
    Overall Status: Accepted with Minor Improvements
    """
    assert reviewer._is_approved_response(response) is True

def test_case_5_completely_valid_project_approved(reviewer):
    response = """
    All checks passed. Clean architecture, error handling present, requirements satisfied.
    
    Overall Status: Accepted
    """
    assert reviewer._is_approved_response(response) is True
