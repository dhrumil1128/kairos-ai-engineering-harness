"""
File: tests/unit/providers/test_response_parser.py

Purpose:
Unit tests for ResponseParser.
"""

from core.providers.response_parser import (
    ResponseParser
)


def test_parser_creation():
    """
    Verify initialization.
    """

    parser = ResponseParser()

    assert parser is not None


def test_parse_response():
    """
    Verify parsing.
    """

    parser = ResponseParser()

    result = parser.parse(
        {
            "provider": "openai",
            "response": "hello",
            "success": True,
        }
    )

    assert (
        result["content"]
        == "hello"
    )


def test_provider_preserved():
    """
    Verify provider field.
    """

    parser = ResponseParser()

    result = parser.parse(
        {
            "provider": "anthropic",
            "response": "test",
            "success": True,
        }
    )

    assert (
        result["provider"]
        == "anthropic"
    )


def test_success_preserved():
    """
    Verify success field.
    """

    parser = ResponseParser()

    result = parser.parse(
        {
            "provider": "gemini",
            "response": "ok",
            "success": True,
        }
    )

    assert (
        result["success"]
        is True
    )


def test_get_content():
    """
    Verify content extraction.
    """

    parser = ResponseParser()

    content = parser.get_content(
        {
            "response": "hello"
        }
    )

    assert content == "hello"


def test_parse_generation_content_extracts_target_code_fence():
    parser = ResponseParser()
    prompt = """
Current File:

calculator/calculator.py
"""
    response = """
Here's the content for the file `calculator/calculator.py`:

```python
class Calculator:
    pass
```
"""

    content = parser.parse_generation_content(
        response,
        prompt=prompt,
    )

    assert content == "class Calculator:\n    pass"


def test_parse_generation_content_keeps_only_current_file_section():
    parser = ResponseParser()
    prompt = """
Current File:

src/main.py
"""
    response = """
Here's the content for the current file `src/main.py`:

from calculator.calculator import Calculator

def main():
    return Calculator()

And here's the content for the file `calculator/calculator.py`:

class Calculator:
    pass
"""

    content = parser.parse_generation_content(
        response,
        prompt=prompt,
    )

    assert "from calculator.calculator import Calculator" in content
    assert "And here's" not in content
    assert "class Calculator" not in content


def test_parse_generation_content_removes_python_explanation():
    parser = ResponseParser()
    prompt = """
Current File:

tests/test_main.py
"""
    response = """
Here's the content for the `tests/test_main.py` file:

import unittest

class TestMain(unittest.TestCase):
    pass

This file contains unit tests for the calculator package.
"""

    content = parser.parse_generation_content(
        response,
        prompt=prompt,
    )

    assert content == "import unittest\n\nclass TestMain(unittest.TestCase):\n    pass"


def test_parse_generation_content_filters_requirements():
    parser = ResponseParser()
    prompt = """
Current File:

requirements.txt
"""
    response = """
**calculator.py**

class Calculator:
    pass

numpy>=1.26
pytest
"""

    content = parser.parse_generation_content(
        response,
        prompt=prompt,
    )

    assert content == "numpy>=1.26\npytest"


def test_parse_generation_content_does_not_return_opening_fence():
    parser = ResponseParser()
    prompt = """
Current File:

src/main.py
"""
    response = """
Here's the content for the current file `src/main.py`:

```python
from calculator.calculator import Calculator


def main():
    return Calculator()
"""

    content = parser.parse_generation_content(
        response,
        prompt=prompt,
    )

    assert content != "```python"
    assert content.startswith("from calculator.calculator import Calculator")
    assert "```python" not in content
