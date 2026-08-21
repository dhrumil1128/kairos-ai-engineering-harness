"""
File: core/providers/real_provider_runtime.py

Purpose:
Coordinate real provider execution.

Why:

Acts as the bridge between
KAIROS provider management
and provider SDK clients.

Future:

V2:
- Real SDK calls

V3:
- Retries

V4:
- Failover

V5:
- Cost-aware routing
"""

from typing import Any

from core.providers.anthropic_sdk_client import (
    AnthropicSDKClient
)

from core.providers.openai_sdk_client import (
    OpenAISDKClient
)

from core.providers.gemini_sdk_client import (
    GeminiSDKClient
)

from core.providers.ollama_sdk_client import (
    OllamaSDKClient
)

from core.providers.nvidia_sdk_client import (
    NvidiaSDKClient
)

from core.parsing.parser_config import (
    ParserConfig
)

from core.parsing.structured_output_parser import (
    StructuredOutputParser
)




class RealProviderRuntime:
    """
    Execute requests using
    provider SDK clients.
    """

    def __init__(self):
        """
        Initialize runtime.
        """
        self.active_project = None

        self.providers = {
            "anthropic":
                AnthropicSDKClient(),

            "openai":
                OpenAISDKClient(),

            "gemini":
                GeminiSDKClient(),
                
            "ollama":
                OllamaSDKClient(),
                

            "nvidia":
                NvidiaSDKClient(),
        }

        self.parser_config = ParserConfig(
            enable_schema_validation=False,
            enable_retry=False,
        )

    


    def provider_exists(
        self,
        provider: str
    ) -> bool:
        """
        Verify provider exists.
        """

        return (
            provider
            in self.providers
        )

    def execute(
        self,
        provider: str,
        prompt: str,
        model: str
    ) -> Any:
        """
        Execute provider request.
        """

        client = (
            self.providers.get(
                provider
            )
        )

        if client is None:
            raise ValueError(
                f"Unknown provider: {provider}"
            )

        
      
        
        response = client.generate(
            prompt=prompt,
            model=model
        )

        return self._parse_structured_response(
            response=response,
            provider=provider,
            model=model,
        )

    def _parse_structured_response(
        self,
        response: Any,
        provider: str,
        model: str
    ) -> Any:
        """
        Parse string responses into structured objects when possible.

        Non-string responses are already structured provider output and
        are returned unchanged. Parse failures also return the original
        response so the provider API keeps its existing behavior.
        """

        if not isinstance(response, str):
            return response

        parser = StructuredOutputParser(
            config=self.parser_config,
            provider=provider,
            model=model,
        )

        try:
            result = parser.parse(
                response
            )
        except Exception:
            return response

        if result.success:
            return result.data

        return response
