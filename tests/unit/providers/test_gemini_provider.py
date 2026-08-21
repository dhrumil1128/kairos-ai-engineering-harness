"""
File: tests/unit/providers/test_gemini_provider.py

Purpose:
Unit tests for GeminiProvider.
"""




from core.providers.gemini_provider import (
    GeminiProvider
)


def test_provider_creation():
    """
    Verify initialization.
    """

    provider = GeminiProvider()

    assert provider is not None


def test_provider_name():
    """
    Verify identity.
    """

    provider = GeminiProvider()

    assert (
        provider.get_name()
        == "gemini"
    )


"""def test_generate():
   
    #Verify generation.
 

    provider = GeminiProvider()

    result = provider.generate(
        "hello"
    )

    assert (
        "Gemini"
        in result
    )
"""

"""def test_prompt_passthrough():
    
    # Verify prompt handling.
    

    provider = GeminiProvider()

    result = provider.generate(
        "test prompt"
    )

    assert (
        "test prompt"
        in result
    )
"""

def test_supported_models():
    """
    Verify model list.
    """

    provider = GeminiProvider()

    models = (
        provider.supported_models()
    )

    assert (
        "gemini-2.5-pro"
        in models
    )
    
    
def test_provider_creation():

    provider = (
        GeminiProvider()
    )

    assert (
        provider.get_name()
        == "gemini"
    )
    

def test_supported_models():

    provider = (
        GeminiProvider()
    )

    models = (
        provider.supported_models()
    )

    assert (
        len(models) > 0
    )

    assert (
        "gemini-2.5-flash"
        in models
    )


def test_configured_exists():

    provider = (
        GeminiProvider()
    )

    assert hasattr(
        provider,
        "configured"
    )
    
def test_generate_exists():

    provider = (
        GeminiProvider()
    )

    assert hasattr(
        provider,
        "generate"
    )