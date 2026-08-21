"""
File: core/providers/provider_runtime.py

Purpose:
Coordinate provider execution.

Why:

Acts as the runtime layer
between requests and providers.

Future:

V2:
- Real SDK execution

V3:
- Retries

V4:
- Failover

V5:
- Parallel execution
"""

from core.providers.provider_executor import (
    ProviderExecutor
)

from core.providers.request_builder import (
    RequestBuilder
)


class ProviderRuntime:
    """
    Execute provider requests.
    """

    def __init__(
        self,
        executor: ProviderExecutor,
        builder: RequestBuilder
    ):
        self.executor = executor
        self.builder = builder

    def run(
        self,
        provider: str,
        model: str,
        prompt: str
    ) -> dict:
        """
        Execute request.
        """

        request = self.builder.build(
            prompt=prompt,
            provider=provider,
            model=model,
        )

        return self.executor.execute(
            request["provider"],
            request["prompt"],
        )