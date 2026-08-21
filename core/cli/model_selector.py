"""
File: core/cli/model_selector.py

Purpose:
Allow users to select
providers and models
at runtime.

Why:

KAIROS should never
hardcode model choices.

Users choose:

Provider
    ↓
Model
    ↓
KAIROS Session

Architecture:

CLI
 ↓
ModelSelector
 ↓
Provider
 ↓
Model
 ↓
Session Config

V1:
- Manual provider selection
- Manual model selection
- Session persistence

V2:
- Auto-discover Ollama models

V3:
- Cost-aware recommendations

V4:
- Capability-aware recommendations

V5:
- Benchmark-driven routing

V6:
- Hybrid provider selection

V7:
- Autonomous model routing

Enterprise:

- Team-wide model policies
- Organization model catalogs
- RBAC provider permissions
- Budget controls
- Centralized governance
"""

from pathlib import Path
import json


class ModelSelector:
    """
    Runtime provider/model selector.
    """

    CONFIG_DIR = (
        Path(".kairos")
    )

    SESSION_FILE = (
        CONFIG_DIR /
        "session.json"
    )

    PROVIDERS = {
        "1": "ollama",
        "2": "openai",
        "3": "gemini",
        "4": "anthropic",
        "5" : "nvidia"
    }
    
    
    NVIDIA_MODELS = {
    "1": "meta/llama-3.3-70b-instruct",
    "2": "meta/llama-3.1-70b-instruct",
    "3": "meta/llama-3.1-8b-instruct",
    "4": "qwen/qwen3.5-122b-a10b",
    "5": "deepseek-ai/deepseek-v4-pro",
    "6": "moonshotai/kimi-k2.6",
    "7": "nvidia/llama-3.3-nemotron-super-49b-v1.5"
   
    }
    
    
    OLLAMA_MODELS = {
        "1": "qwen3:8b",
        "2": "llama3.2:3b",
        "3": "deepseek-r1",
        "4": "mistral",
        "5": "qwen3:4b",
        
    }

    OPENAI_MODELS = {
        "1": "gpt-5",
        "2": "gpt-5-mini",
    }

    GEMINI_MODELS = {
        "1": "gemini-2.5-pro",
        "2": "gemini-2.5-flash",
    }

    ANTHROPIC_MODELS = {
        "1": "claude-opus",
        "2": "claude-sonnet",
        "3": "claude-haiku",
    }

    def __init__(self):
        """
        Initialize selector.
        """

        self.CONFIG_DIR.mkdir(
            exist_ok=True
        )
        
    def get_providers(
        self
    ):
        return self.PROVIDERS



    def get_models(
        self,
        provider: str
    ):
        """
        Return available models
        for provider.
        """

        model_map = {
            "ollama":
                self.OLLAMA_MODELS,

            "openai":
                self.OPENAI_MODELS,

            "gemini":
                self.GEMINI_MODELS,

            "anthropic":
                self.ANTHROPIC_MODELS,
                
            "nvidia":
                self.NVIDIA_MODELS,
        }

        return model_map.get(
            provider,
            {}
        )
        
        
        
        
    def select_provider(self):
        """
        Select provider.
        """

        print(
            "\nAvailable Providers\n"
        )

        for key, value in (
            self.PROVIDERS.items()
        ):
            print(
                f"{key}. {value}"
            )

        choice = input(
            "\nSelect Provider: "
        )

        return self.PROVIDERS.get(
            choice
        )

    def select_model(
        self,
        provider: str
    ):
        """
        Select model.
        """

        model_map = {
            "ollama":
                self.OLLAMA_MODELS,

            "openai":
                self.OPENAI_MODELS,

            "gemini":
                self.GEMINI_MODELS,

            "anthropic":
                self.ANTHROPIC_MODELS,
                
            "nvidia":
                self.NVIDIA_MODELS,
        }

        models = (
            model_map.get(
                provider,
                {}
            )
        )

        print(
            f"\nAvailable {provider} Models\n"
        )

        for key, value in (
            models.items()
        ):
            print(
                f"{key}. {value}"
            )

        choice = input(
            "\nSelect Model: "
        )

        return models.get(
            choice
        )

    def save_session(
        self,
        provider: str,
        model: str
    ):
        """
        Save session.
        """

        data = {
            "provider": provider,
            "model": model
        }

        with open(
            self.SESSION_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load_session(self):
        """
        Load session.
        """

        if (
            not self.SESSION_FILE.exists()
        ):
            return None

        with open(
            self.SESSION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    def configure(self):
        """
        Configure session.
        """

        provider = (
            self.select_provider()
        )

        model = (
            self.select_model(
                provider
            )
        )

        self.save_session(
            provider,
            model
        )

        print(
            "\n[KAIROS]"
        )

        print(
            f"Provider = {provider}"
        )

        print(
            f"Model = {model}"
        )

        return {
            "provider": provider,
            "model": model
        }