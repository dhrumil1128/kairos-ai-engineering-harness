"""
File: core/parsing/schema_validator.py

Purpose:
Validate parsed data against an optional schema.

Why:
Schema validation ensures parsed data matches
expected structure without requiring the
parser to know about specific data models.

Architecture Position:

Structured Output Parser
    ↓
SchemaValidator
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import re


@dataclass
class ValidationResult:
    """
    Result of schema validation.

    Attributes:
        success: Whether validation passed.
        data: Validated data (may be normalized).
        failure_reason: Reason for failure.
        warnings: List of validation warnings.
    """
    success: bool = False
    data: Any = None
    failure_reason: str = ""
    warnings: List[str] = field(default_factory=list)


class SchemaValidator:
    """
    Validates parsed data against a schema.

    Supports:
    - Type checking
    - Required field checking
    - Pattern validation
    - Nested structure validation
    """

    def __init__(self):
        """Initialize the schema validator."""
        self.required_fields = ["type"]

    def validate(
        self,
        data: Any,
        schema: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Validate data against a schema.

        Args:
            data: Parsed data to validate.
            schema: Optional schema definition.

        Returns:
            ValidationResult with success status.
        """
        if schema is None:
            # No schema provided, basic validation only
            return self._basic_validation(data)

        return self._validate_with_schema(data, schema)

    def _basic_validation(
        self,
        data: Any
    ) -> ValidationResult:
        """
        Perform basic validation without schema.

        Args:
            data: Data to validate.

        Returns:
            ValidationResult.
        """
        if data is None:
            return ValidationResult(
                success=False,
                failure_reason="Data is None"
            )

        if isinstance(data, dict):
            if not data:
                return ValidationResult(
                    success=False,
                    failure_reason="Empty dictionary"
                )
            return ValidationResult(success=True, data=data)

        if isinstance(data, list):
            if not data:
                return ValidationResult(
                    success=False,
                    failure_reason="Empty list"
                )
            return ValidationResult(success=True, data=data)

        # Primitive types are valid
        return ValidationResult(success=True, data=data)

    def _validate_with_schema(
        self,
        data: Any,
        schema: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate data against a schema definition.

        Args:
            data: Data to validate.
            schema: Schema definition.

        Returns:
            ValidationResult.
        """
        # Check type constraint
        expected_type = schema.get("type")
        if expected_type:
            if not self._check_type(data, expected_type):
                return ValidationResult(
                    success=False,
                    failure_reason=f"Type mismatch: expected {expected_type}, got {type(data).__name__}"
                )

        # Check required fields for dicts
        if isinstance(data, dict):
            required = schema.get("required", [])
            missing = []

            for field in required:
                if field not in data:
                    missing.append(field)

            if missing:
                return ValidationResult(
                    success=False,
                    failure_reason=f"Missing required fields: {', '.join(missing)}"
                )

            # Validate nested properties
            properties = schema.get("properties", {})
            for key, value in data.items():
                if key in properties:
                    nested_schema = properties[key]
                    nested_result = self._validate_with_schema(value, nested_schema)

                    if not nested_result.success:
                        return ValidationResult(
                            success=False,
                            failure_reason=f"Validation failed for field '{key}': {nested_result.failure_reason}"
                        )

            # Check for extra fields if strict
            if schema.get("strict", False):
                allowed = set(properties.keys())
                extra = set(data.keys()) - allowed
                if extra:
                    return ValidationResult(
                        success=False,
                        failure_reason=f"Extra fields not allowed: {', '.join(extra)}"
                    )

        # Check items for lists
        if isinstance(data, list) and "items" in schema:
            item_schema = schema["items"]
            for i, item in enumerate(data):
                item_result = self._validate_with_schema(item, item_schema)
                if not item_result.success:
                    return ValidationResult(
                        success=False,
                        failure_reason=f"Validation failed for list item {i}: {item_result.failure_reason}"
                    )

        return ValidationResult(success=True, data=data)

    def _check_type(
        self,
        value: Any,
        expected_type: str
    ) -> bool:
        """
        Check if value matches expected type.

        Args:
            value: Value to check.
            expected_type: Expected type name.

        Returns:
            True if type matches.
        """
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }

        if expected_type not in type_mapping:
            return True  # Unknown type, accept

        expected = type_mapping[expected_type]

        if expected_type == "number":
            return isinstance(value, (int, float)) and not isinstance(value, bool)

        return isinstance(value, expected)

    def validate_pattern(
        self,
        value: str,
        pattern: str
    ) -> bool:
        """
        Validate string against a pattern.

        Args:
            value: String value.
            pattern: Regex pattern.

        Returns:
            True if matches pattern.
        """
        try:
            return bool(re.match(pattern, value))
        except re.error:
            return False