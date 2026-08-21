"""
File:
tests/integration/providers/
test_ollama_integration.py

Purpose:
Real Ollama integration test.
"""

import pytest

from core.providers.ollama_sdk_client import (
    OllamaSDKClient
)


@pytest.mark.integration
def test_ollama_real_generation():
    """
    Verify real Ollama response.
    """

    client = OllamaSDKClient()

    if not client.health_check():

        pytest.skip(
            "Ollama server not running"
        )

    response = client.generate(
        prompt=(
            "Reply with exactly: "
            "KAIROS_OLLAMA_OK"
        ),
        model="llama3.2:3b"
    )

    print(
        "\nOllama Response:"
    )

    print(response)

    assert response is not None

    assert (
        len(
            response.strip()
        )
        > 0
    )