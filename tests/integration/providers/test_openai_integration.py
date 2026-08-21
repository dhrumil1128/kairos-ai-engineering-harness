"""
File:
tests/integration/providers/
test_openai_integration.py

Purpose:
Real OpenAI integration test.
"""

import os

import pytest
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
RUN_OPENAI_TESTS = os.getenv(
    "RUN_OPENAI_TESTS",
    "false"
).lower() == "true"



API_KEY = os.getenv(
    "OPENAI_API_KEY"
)


@pytest.mark.integration
@pytest.mark.skipif(
    (
        not API_KEY
        or not RUN_OPENAI_TESTS
    ),
    reason=(
        "OpenAI integration disabled"
    )
)



def test_openai_real_generation():
    """
    Verify real OpenAI response.
    """

    client = OpenAI(
        api_key=API_KEY
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input="Reply with exactly: KAIROS_OPENAI_OK"
    )

    text = response.output_text

    print("\nOpenAI Response:")
    print(text)

    assert text is not None
    assert len(text.strip()) > 0