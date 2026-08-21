"""
File: tests/unit/context/test_document_parser.py

Purpose:
Unit tests for DocumentParser.
"""

from core.context.document_parser import (
    DocumentParser
)


def test_parser_creation():
    """
    Verify initialization.
    """

    parser = DocumentParser()

    assert parser is not None


def test_parse_document():
    """
    Verify parsing.
    """

    parser = DocumentParser()

    result = parser.parse(
        "Line 1\nLine 2"
    )

    assert len(result) == 2


def test_empty_document():
    """
    Verify empty content.
    """

    parser = DocumentParser()

    assert (
        parser.parse("")
        == []
    )


def test_section_count():
    """
    Verify section count.
    """

    parser = DocumentParser()

    count = parser.section_count(
        "A\nB\nC"
    )

    assert count == 3


def test_strip_blank_lines():
    """
    Verify blank line removal.
    """

    parser = DocumentParser()

    result = parser.parse(
        "A\n\nB\n\nC"
    )

    assert len(result) == 3