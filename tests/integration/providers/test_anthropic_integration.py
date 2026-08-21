"""
File:
tests/integration/providers/
test_anthropic_integration.py

Purpose:
Real Anthropic integration test.
"""

import os

import pytest
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

API_KEY = os.getenv(
    "ANTHROPIC_API_KEY"
)


@pytest.mark.integration
@pytest.mark.skipif(
    not API_KEY,
    reason="ANTHROPIC_API_KEY not configured"
)
def test_anthropic_real_generation():
    """
    Verify real Anthropic response.
    """

    client = Anthropic(
        api_key=API_KEY
    )

    response = client.messages.create(
        model="claude-sonnet-4-0",
        max_tokens=50,
        messages=[
            {
                "role": "user",
                "content": (
                    "Reply with exactly: "
                    "KAIROS_ANTHROPIC_OK"
                )
            }
        ]
    )

    text = response.content[0].text

    print("\nAnthropic Response:")
    print(text)

    assert text is not None
    assert len(text.strip()) > 0