"""
File: core/providers/provider_manager.py

Purpose:
Manage provider execution.

Why:

Provides a single entry point
for provider routing and
execution.

Architecture:

Agent
 ↓
ProviderManager
 ↓
ModelRouter
 ↓
RealProviderRuntime
 ↓
SDK Client
 ↓
LLM Response

V1:
- Provider execution

V2:
- Provider failover

V3:
- Health-aware routing

V4:
- Cost-aware routing

V5:
- Multi-provider orchestration
"""

# Provider registry.
from core.providers.provider_registry import (
    ProviderRegistry
)

# Model router.
from core.providers.model_router import (
    ModelRouter
)

# Runtime executor.
from core.providers.real_provider_runtime import (
    RealProviderRuntime
)

from core.cli.model_selector import (
    ModelSelector
)

from core.providers.response_parser import (
    ResponseParser
)


from core.logging.kairos_logger import KairosLogger

class ProviderManager:
    """
    Manage providers.
    """

    def __init__(
        self,
        registry: ProviderRegistry
    ):
        """
        Initialize manager.
        """

        # Store registry.
        self.registry = registry

        # Create router.
        self.router = (
            ModelRouter()
        )

        # Create runtime.
        self.runtime = (
            RealProviderRuntime()
        )
        
        # KAIROS logger.
        self.logger = KairosLogger(
            "kairos"
        )
        
        
        self.model_selector = (
            ModelSelector()
        )

        self.response_parser = (
            ResponseParser()
        )
        
        

    def register_provider(
        self,
        name: str,
        provider: object
    ) -> None:
        """
        Register provider.
        """

        self.registry.register(
            name,
            provider
        )

    def get_provider(
        self,
        name: str
    ) -> object | None:
        """
        Retrieve provider.
        """

        return self.registry.get(
            name
        )

    def provider_exists(
        self,
        name: str
    ) -> bool:
        """
        Check provider existence.
        """

        return self.registry.exists(
            name
        )

    def provider_count(
        self
    ) -> int:
        """
        Return provider count.
        """

        return self.registry.count()

    def execute(
        self,
        task_type: str,
        prompt: str
    ) -> str:
        """
        Execute provider request.
        """



        session = (
            self.model_selector
            .load_session()
        )

        if not session:

            raise RuntimeError(
                "No active model session."
            )

        provider = (
            session["provider"]
        )

        model = (
            session["model"]
        )


        # Route task.
        route = {

        "provider":
            provider,

        "model":
            model
    }
        
        # statement 
        self.logger.debug(
        f"Task={task_type}"
        )

        self.logger.debug(
            f"Provider={route['provider']}"
        )

        self.logger.debug(
            f"Model={route['model']}"
        )

        # Execute request.
        response = (
            self.runtime.execute(
                provider=(
                    route["provider"]
                ),
                model=(
                    route["model"]
                ),
                prompt=prompt
            )
        )

        self._log_content_diagnostic(
            "LLM provider response",
            response
        )

        if (
            task_type == "coding"
            and "Current File:" in prompt
            and isinstance(response, str)
        ):
            self._log_content_diagnostic(
                "Parser input",
                response
            )

            parsed_response = self.response_parser.parse_generation_content(
                response,
                prompt=prompt
            )

            self._log_content_diagnostic(
                "Parser output",
                parsed_response
            )

            return parsed_response

        return response

    def _log_content_diagnostic(
        self,
        stage: str,
        content
    ) -> None:
        """
        Log content flow diagnostics without mutating the response.
        """

        is_none = content is None
        text = "" if content is None else str(content)
        is_empty = text == ""
        preview = text[:200].replace(
            "\n",
            "\\n"
        )

        self.logger.debug(
            (
                "[CONTENT TRACE] "
                f"{stage} | "
                f"length={len(text)} | "
                f"is_none={is_none} | "
                f"is_empty={is_empty} | "
                f"first_200={preview}"
            )
        )
