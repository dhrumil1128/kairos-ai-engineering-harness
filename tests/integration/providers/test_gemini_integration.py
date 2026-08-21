"""
File: tests/integration/providers/test_gemini_integration.py

Purpose:
Real Gemini integration test.

Requires:

GEMINI_API_KEY
"""

from email.mime import text
import os

import pytest

from google import genai

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


@pytest.mark.integration
@pytest.mark.skipif(
    not API_KEY,
    reason="GEMINI_API_KEY not configured"
)
def test_gemini_real_generation():
    """
    Verify real Gemini response.
    """

    client = genai.Client(
        api_key=API_KEY
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Reply with exactly: KAIROS_OK and Say Hello From Gemini."
    )

    text = response.text
    print("\nGemini Response:")
    print(text)

    assert text is not None
    assert len(text.strip()) > 0