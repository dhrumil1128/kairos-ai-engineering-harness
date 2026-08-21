"""
File: core/providers/request_builder.py

Purpose:
Build standardized provider requests.

Why:

Different providers require
different request formats.

KAIROS should generate a
consistent internal request
object before execution.

Future:

V2:
- Model selection

V3:
- Tool calling

V4:
- System prompts

V5:
- Structured outputs
"""


class RequestBuilder:
    """
    Build provider requests.
    """

    def build(
        self,
        prompt: str,
        provider: str,
        model: str
    ) -> dict:
        """
        Build request payload.
        """

        return {
            "provider": provider,
            "model": model,
            "prompt": prompt,
        }

    def validate(
        self,
        request: dict
    ) -> bool:
        """
        Validate request.
        """

        required = [
            "provider",
            "model",
            "prompt",
        ]

        return all(
            field in request
            for field in required
        )