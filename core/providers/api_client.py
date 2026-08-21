"""
File: core/providers/api_client.py

Purpose:
Handle provider API requests.

Why:

Provides a unified interface
for communicating with model
providers.

Future:

V2:
- Real HTTP requests

V3:
- Retry logic

V4:
- Streaming responses

V5:
- Multi-provider failover
"""


class APIClient:
    """
    API communication layer.
    """

    def send_request(
        self,
        provider: str,
        prompt: str
    ) -> dict:
        """
        Send request.

        Parameters:
            provider:
                Provider name.

            prompt:
                User prompt.

        Returns:
            Mock API response.
        """

        return {
            "provider": provider,
            "prompt": prompt,
            "response": (
                f"Response from {provider}"
            ),
            "success": True,
        }

    def is_successful(
        self,
        response: dict
    ) -> bool:
        """
        Check response status.
        """

        return response.get(
            "success",
            False
        )