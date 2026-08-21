"""
File: core/providers/provider_executor.py

Purpose:
Execute provider requests.

Why:

Coordinates provider execution,
API communication, and response
parsing.

Future:

V2:
- Real SDK integration

V3:
- Retry handling

V4:
- Streaming support

V5:
- Multi-provider execution
"""

from core.providers.api_client import (
    APIClient
)

from core.providers.response_parser import (
    ResponseParser
)


class ProviderExecutor:
    """
    Execute provider requests.
    """

    def __init__(
        self,
        api_client: APIClient,
        parser: ResponseParser
    ):
        """
        Initialize executor.
        """

        self.api_client = api_client
        self.parser = parser

    def execute(
        self,
        provider: str,
        prompt: str
    ) -> dict:
        """
        Execute request.

        Parameters:
            provider:
                Provider name.

            prompt:
                User prompt.

        Returns:
            Standardized response.
        """

        raw_response = (
            self.api_client.send_request(
                provider,
                prompt
            )
        )

        return self.parser.parse(
            raw_response
        )