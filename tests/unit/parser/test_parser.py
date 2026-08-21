"""
Unit Tests for StructuredOutputParser

Run:
    pytest tests/unit/parser/test_parser.py -vv
"""

import pytest

from core.parsing.structured_output_parser import StructuredOutputParser
from core.parsing.parser_config import ParserConfig
from core.parsing.parse_result import ParseStage


@pytest.fixture
def parser():
    config = ParserConfig(
        enable_schema_validation=False,
        enable_retry=False,
        enable_repair=True,
    )
    return StructuredOutputParser(config=config)


def test_valid_json(parser):
    result = parser.parse('{"name":"KAIROS","version":"1.0"}')

    assert result.success is True
    assert result.data["name"] == "KAIROS"
    assert result.data["version"] == "1.0"
    assert result.confidence == 1.0


def test_markdown_json(parser):
    text = """
```json
{
    "project": "KAIROS",
    "type": "CLI"
}
```
"""

    result = parser.parse(text)

    assert result.success is True
    assert result.data["project"] == "KAIROS"
    assert result.data["type"] == "CLI"


def test_trailing_comma_repair(parser):
    text = """
{
    "name": "KAIROS",
    "version": "1.0",
}
"""

    result = parser.parse(text)

    assert result.success is True
    assert result.data["name"] == "KAIROS"
    assert result.confidence >= 0.9


def test_comment_repair(parser):
    text = """
{
    "name": "KAIROS",
    // this is a comment
    "version": "1.0"
}
"""

    result = parser.parse(text)

    assert result.success is True
    assert result.data["version"] == "1.0"


def test_unquoted_key_repair(parser):
    text = """
{
    "name" : "KAIROS"
}
"""

    result = parser.parse(text)

    assert result.success is True
    assert result.data["name"] == "KAIROS"


def test_invalid_json(parser):
    result = parser.parse("Hello World. This is not JSON.")

    assert result.success is False
    assert result.stage == ParseStage.FAILED
    assert result.failure_reason is not None


def test_metrics(parser):
    parser.reset_metrics()

    parser.parse('{"a":1}')
    parser.parse("Not JSON")

    metrics = parser.get_metrics()

    assert metrics is not None


def test_parse_time(parser):
    result = parser.parse('{"hello":"world"}')

    assert result.parse_time_ms >= 0


def test_stage_exists(parser):
    result = parser.parse('{"x":1}')

    assert result.stage is not None


def test_return_type(parser):
    result = parser.parse('{"framework":"KAIROS"}')

    assert hasattr(result, "success")
    assert hasattr(result, "data")
    assert hasattr(result, "confidence")
    assert hasattr(result, "stage")
    assert hasattr(result, "parse_time_ms")