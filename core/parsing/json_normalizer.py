"""
File: core/parsing/json_normalizer.py

Purpose:
Normalize raw LLM output for JSON parsing.

Why:
LLMs often return text with formatting issues,
whitespace problems, or encoding issues that
prevent clean JSON parsing.

Architecture Position:

Structured Output Parser
    ↓
JsonNormalizer
"""

import re
import html
import unicodedata
from typing import Optional


class JsonNormalizer:
    """
    Normalizes raw text for JSON parsing.

    Handles:
    - Whitespace normalization
    - Control character removal
    - HTML entity decoding
    - Unicode normalization
    - Code block stripping
    """

    # Pattern to match code blocks (``` or ```json)
    CODE_BLOCK_PATTERN = re.compile(
        r"```(?:json)?\s*\n?(.*?)\n?```",
        re.DOTALL | re.IGNORECASE
    )

    # Pattern to match markdown code blocks without language
    MD_CODE_BLOCK_PATTERN = re.compile(
        r"```\s*\n?(.*?)\n?```",
        re.DOTALL
    )

    def normalize(
        self,
        raw_text: str
    ) -> str:
        """
        Normalize raw text for JSON parsing.

        Args:
            raw_text: Raw LLM output.

        Returns:
            Normalized text ready for JSON extraction.
        """
        if not raw_text:
            return ""

        normalized = raw_text

        # Step 1: Decode HTML entities
        normalized = html.unescape(normalized)

        # Step 2: Unicode normalization (NFKC)
        normalized = unicodedata.normalize(
            "NFKC",
            normalized
        )

        # Step 3: Remove non-printable control characters
        normalized = self._remove_control_characters(normalized)

        # Step 4: Strip code blocks
        normalized = self._strip_code_blocks(normalized)

        # Step 5: Normalize whitespace
        normalized = self._normalize_whitespace(normalized)

        # Step 6: Trim leading/trailing whitespace
        normalized = normalized.strip()

        return normalized

    def _remove_control_characters(
        self,
        text: str
    ) -> str:
        """
        Remove control characters that interfere with JSON.

        Args:
            text: Input text.

        Returns:
            Text with control characters removed.
        """
        # Remove control characters except newline, tab, and carriage return
        result = []
        for char in text:
            code = ord(char)
            if (
                code == 0x09  # tab
                or code == 0x0A  # newline
                or code == 0x0D  # carriage return
                or code > 0x1F  # printable or extended
            ):
                result.append(char)

        return "".join(result)

    def _strip_code_blocks(
        self,
        text: str
    ) -> str:
        """
        Strip markdown code blocks to extract raw content.

        Args:
            text: Input text possibly containing code blocks.

        Returns:
            Text with code blocks stripped to content.
        """
        # First, try to match json code blocks
        match = self.CODE_BLOCK_PATTERN.search(text)
        if match:
            return match.group(1).strip()

        # Then try generic code blocks
        match = self.MD_CODE_BLOCK_PATTERN.search(text)
        if match:
            content = match.group(1).strip()
            # Check if it looks like JSON
            if content.startswith(("{", "[")) or '":' in content:
                return content

        return text

    def _normalize_whitespace(
        self,
        text: str
    ) -> str:
        """
        Normalize whitespace in text.

        Args:
            text: Input text.

        Returns:
            Text with normalized whitespace.
        """
        # Replace multiple spaces with single space
        text = re.sub(r"[ ]{2,}", " ", text)

        # Replace multiple newlines with single newline
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Replace mixed line endings with Unix style
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        return text

    def is_json_like(
        self,
        text: str
    ) -> bool:
        """
        Check if text appears to be JSON-like.

        Args:
            text: Input text.

        Returns:
            True if text appears to be JSON.
        """
        text = text.strip()
        return (
            text.startswith("{") or
            text.startswith("[") or
            text.startswith('"') or
            text.startswith("'")
        )