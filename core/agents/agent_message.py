"""
File: core/agents/agent_message.py

Purpose:
Standard communication protocol
between KAIROS agents.

Why:

All agents should communicate using
a common message format.

Without this:

Planner → Architect
Architect → Coder

would all use different structures.

With AgentMessage:

Every agent speaks the same language.

Architecture:

PlannerAgent
      ↓
AgentMessage
      ↓
ArchitectAgent

ArchitectAgent
      ↓
AgentMessage
      ↓
CoderAgent

Future:

Agent Router
Agent Orchestrator
Parallel Executor
"""

# Dataclass support.
from dataclasses import dataclass

# Structured typing.
from typing import Any


@dataclass
class AgentMessage:
    """
    Standard message exchanged
    between agents.
    """

    # Sender agent.
    sender: str

    # Receiver agent.
    receiver: str

    # Message category.
    message_type: str

    # Message content.
    payload: Any