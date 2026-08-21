"""
File:
tests/integration/providers/
test_kairos_gemini_runtime.py

Purpose:
Verify full KAIROS Gemini runtime.
"""

import os

import pytest

from dotenv import load_dotenv

from core.providers.real_provider_runtime import (
    RealProviderRuntime
)

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


@pytest.mark.integration
@pytest.mark.skipif(
    not API_KEY,
    reason="GEMINI_API_KEY not configured"
)
def test_kairos_runtime_gemini():
    """
    Verify KAIROS runtime can
    execute Gemini requests.
    """

    runtime = (
        RealProviderRuntime()
    )

    result = runtime.execute(
        provider="gemini",
        prompt="Reply with KAIROS_RUNTIME_OK",
        model="gemini-2.5-flash-lite"
    )

    print("\nRuntime Response:")
    print(result)

    assert result is not None
    assert len(
        str(result).strip()
    ) > 0