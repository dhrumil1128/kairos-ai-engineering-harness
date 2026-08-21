"""
File: core/providers/model_router.py

Purpose:
Select the most appropriate
model for a task.

Why:

Users choose the provider.

KAIROS chooses the model.

Architecture:

Agent
 ↓
ModelRouter
 ↓
Provider
 ↓
Model
 ↓
Provider Runtime
 ↓
LLM Response

V1:
- Provider-specific routing

V2:
- Cost-aware routing

V3:
- Capability-aware routing

V4:
- Provider benchmarking

V5:
- Autonomous model selection

V6:
- Dynamic optimization

V7:
- Multi-provider orchestration
"""
from pathlib import Path
import json

class ModelRouter:
    """
    Route tasks to models.
    """



    def get_session_model(
        self
    ):
        """
        Load selected model
        from session.json.
        """

        session_file = (
            Path(".kairos")
            / "session.json"
        )

        if not session_file.exists():

            return None

        with open(
            session_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        return data.get(
            "model"
        )
    
    
    
    
    
    def get_session_provider(
        self
    ):
        """
        Load selected provider
        from session.json.
        """

    

        session_file = (
            Path(".kairos")
            / "session.json"
        )

        if not session_file.exists():

            return None

        with open(
            session_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        return data.get(
            "provider"
        )
    
    

    def route(
        self,
        task_type: str,
        provider: str
    ) -> dict:
        """
        Select provider model.
        """

        

        # Normalize provider.
        provider = (
            provider.lower()
        )
        
        selected_provider = (
            self.get_session_provider()
        )
        
        selected_model = (
            self.get_session_model()
        )

       # User-selected session
       # overrides routing.

        if (
            selected_provider
            and
            selected_model
        ):
            return {
                "provider":
                    selected_provider,
                "model":
                    selected_model
            }


# ----------------------------------
# Fallback Routing
# ----------------------------------
#
# Why:
#
# Session-based model selection
# should always take priority.
#
# However, if:
#
# - session.json is missing
# - session.json is corrupted
# - no model has been selected
# - first startup has not completed
#
# KAIROS must still function.
#
# Therefore we keep default
# provider routing as a safety
# mechanism.
#
# Future Versions:
#
# V2:
# - Session validation
#
# V3:
# - Automatic recovery
#
# V4:
# - Provider failover
#
# V5:
# - Multi-model routing
#
# Enterprise:
# - Organization defaults
# - Policy enforcement
# - Team model catalogs
#
# ----------------------------------



        if provider == "ollama":

            return {
                "provider": "ollama",
                "model": "qwen3:8b"
            }

        elif provider == "gemini":

            return {
                "provider": "gemini",
                "model": "gemini-2.5-flash"
            }

        elif provider == "openai":

            return {
                "provider": "openai",
                "model": "gpt-5"
            }

        elif provider == "anthropic":

            return {
                "provider": "anthropic",
                "model": "claude-sonnet"
            }
        
        
       
                
                
        