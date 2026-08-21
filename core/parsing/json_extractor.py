"""
File: core/parsing/json_extractor.py

Purpose:
Extract JSON from LLM responses.

Why:
LLMs may return text with JSON embedded or
mixed with other content. This extractor
isolates the JSON portion.

Architecture Position:

Structured Output Parser
    ↓
JsonExtractor
"""

import re
from typing import Optional


class JsonExtractor:
    """
    Extracts JSON from LLM responses.

    Handles:
    - Bare JSON objects and arrays
    - JSON with text prefix/suffix
    - Code blocks with JSON
    - Partial JSON extraction
    """

    # Pattern to match JSON objects
    JSON_OBJECT_PATTERN = re.compile(
        r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}",
        re.DOTALL
    )

    # Pattern to match JSON arrays
    JSON_ARRAY_PATTERN = re.compile(
        r"\[(?:[^\[\]]|(?:\[[^\[\]]*\]))*\]",
        re.DOTALL
    )

    # Pattern to match JSON with key-value pairs
    JSON_KV_PATTERN = re.compile(
        r"\{[^{}]*\}",
        re.DOTALL
    )

    def extract(
        self,
        text: str
    ) -> str:
        """
        Extract JSON from text.

        Args:
            text: Normalized text from JsonNormalizer.

        Returns:
            Extracted JSON string, or original text if no JSON found.
        """
        if not text:
            return ""

        # First, check if the entire text is already valid JSON
        stripped = text.strip()
        if self._is_valid_json_start(stripped):
            return stripped

        # Try to find JSON object
        json_obj = self._extract_json_object(stripped)
        if json_obj:
            return json_obj

        # Try to find JSON array
        json_arr = self._extract_json_array(stripped)
        if json_arr:
            return json_arr

        # Return original text if no JSON found
        return stripped

    def _is_valid_json_start(
        self,
        text: str
    ) -> bool:
        """
        Check if text starts with valid JSON.

        Args:
            text: Text to check.

        Returns:
            True if text starts with JSON.
        """
        return text.startswith("{") or text.startswith("[")

    def _extract_json_object(
        self,
        text: str
    ) -> Optional[str]:
        """
        Extract a JSON object from text.

        Args:
            text: Input text.

        Returns:
            Extracted JSON object or None.
        """
        start_idx = text.find("{")
        if start_idx == -1:
            return None

        # Find matching closing brace
        brace_count = 0
        for i, char in enumerate(text[start_idx:], start=start_idx):
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    return text[start_idx:i + 1]

        # Unbalanced braces, return partial if we have content
        if brace_count > 0 and start_idx >= 0:
            return text[start_idx:]

        return None

    def _extract_json_array(
        self,
        text: str
    ) -> Optional[str]:
        """
        Extract a JSON array from text.

        Args:
            text: Input text.

        Returns:
            Extracted JSON array or None.
        """
        start_idx = text.find("[")
        if start_idx == -1:
            return None

        # Find matching closing bracket
        bracket_count = 0
        for i, char in enumerate(text[start_idx:], start=start_idx):
            if char == "[":
                bracket_count += 1
            elif char == "]":
                bracket_count -= 1
                if bracket_count == 0:
                    return text[start_idx:i + 1]

        # Unbalanced brackets, return partial if we have content
        if bracket_count > 0 and start_idx >= 0:
            return text[start_idx:]

        return None

    def find_json_boundaries(
        self,
        text: str
    ) -> tuple[Optional[int], Optional[int]]:
        """
        Find the start and end boundaries of JSON in text.

        Args:
            text: Input text.

        Returns:
            Tuple of (start_index, end_index) or (None, None).
        """
        if not text:
            return None, None

        json_obj = self._extract_json_object(text)
        if json_obj:
            start = text.find(json_obj)
            return start, start + len(json_obj)

        json_arr = self._extract_json_array(text)
        if json_arr:
            start = text.find(json_arr)
            return start, start + len(json_arr)

        return None, None