"""
File: core/providers/sdk_adapter.py

Purpose:
Provide a unified interface
between KAIROS and provider SDKs.

Why:

Each provider SDK behaves
differently.

KAIROS should interact through
a single abstraction layer.

Future:

V2:
- Real SDK connections

V3:
- Streaming support

V4:
- Tool calling

V5:
- Multi-modal support
"""


class SDKAdapter:
    """
    SDK abstraction layer.
    """

    def adapt_request(
        self,
        provider: str,
        model: str,
        prompt: str
    ) -> dict:
        """
        Convert request into
        standardized SDK format.
        """

        return {
            "provider": provider,
            "model": model,
            "prompt": prompt,
        }

    def adapt_response(
        self,
        provider: str,
        response: str
    ) -> dict:
        """
        Convert SDK response into
        KAIROS format.
        """

        return {
            "provider": provider,
            "content": response,
            "success": True,
        }

    def is_valid(
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