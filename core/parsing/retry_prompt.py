"""
File: core/parsing/retry_prompt.py

Purpose:
Generate retry prompts for failed parsing.

Why:
When parsing fails, we may need to ask the
LLM to retry with a more explicit prompt.
This module handles that generation.

Architecture Position:

Structured Output Parser
    ↓
RetryPrompt
"""

from typing import Optional, Any


class RetryPrompt:
    """
    Generates retry prompts for parsing failures.

    Provides prompts that can be sent back to the
    LLM to request properly formatted output.
    """

    # Default instruction for retry
    DEFAULT_INSTRUCTION = (
        "Please respond with valid JSON only. "
        "Do not include any explanations or markdown."
    )

    # Template for retry prompts
    RETRY_TEMPLATE = (
        "Parsing failed. {instruction}\n\n"
        "Original: {original}\n\n"
        "Format: {format_hint}"
    )

    def __init__(
        self,
        instruction: Optional[str] = None,
        format_hint: Optional[str] = None
    ):
        """
        Initialize retry prompt generator.

        Args:
            instruction: Custom instruction for retry.
            format_hint: Custom format hint.
        """
        self.instruction = instruction or self.DEFAULT_INSTRUCTION
        self.format_hint = format_hint or "JSON object with key-value pairs"

    def generate(
        self,
        original_response: str,
        parse_result: dict[str, Any]
    ) -> str:
        """
        Generate a retry prompt.

        Args:
            original_response: The original LLM response.
            parse_result: The parse result details.

        Returns:
            Retry prompt string.
        """
        return self.RETRY_TEMPLATE.format(
            instruction=self.instruction,
            original=original_response[:500],  # Truncate for context
            format_hint=self.format_hint
        )

    def generate_strict_json_prompt(
        self,
        schema_description: Optional[str] = None
    ) -> str:
        """
        Generate a strict JSON-only prompt.

        Args:
            schema_description: Optional schema description.

        Returns:
            Strict JSON prompt.
        """
        prompt = "Respond with valid JSON only. No explanations."

        if schema_description:
            prompt += f"\n\nSchema: {schema_description}"

        return prompt

    def generate_with_format_hint(
        self,
        format_spec: str
    ) -> str:
        """
        Generate prompt with specific format hint.

        Args:
            format_spec: Expected format specification.

        Returns:
            Prompt with format hint.
        """
        return (
            f"Respond with valid JSON in this format:\n"
            f"{format_spec}\n\n"
            f"Only output the JSON, nothing else."
        )

    @staticmethod
    def simple_retry_prompt() -> str:
        """
        Generate a simple retry prompt.

        Returns:
            Simple retry prompt.
        """
        return (
            "Please return your response as valid JSON only. "
            "Do not include any markdown formatting or explanations."
        )

    @staticmethod
    def schema_retry_prompt(schema_type: str) -> str:
        """
        Generate a retry prompt for a specific schema type.

        Args:
            schema_type: Type of schema expected.

        Returns:
            Schema-specific retry prompt.
        """
        return (
            f"Please return a valid JSON {schema_type} object only. "
            f"Do not include any explanations or markdown."
        )