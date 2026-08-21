"""
File: core/shared/constants.py

Purpose:
Global constants used throughout KAIROS.

Why:
Avoid hardcoded values scattered across the codebase.

Architecture Position:

Agents
Memory
Security
Runtime
Executor
Token Engine
        ↓
     Constants
"""

# ============================================================
# APPLICATION
# ============================================================

APP_NAME = "KAIROS"
APP_VERSION = "0.1.0"

# ============================================================
# RECURSIVE EXECUTION ENGINE
# ============================================================

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 2

# ============================================================
# RUNTIME
# ============================================================

DEFAULT_TIMEOUT_SECONDS = 60
MAX_CONCURRENT_TASKS = 10

# ============================================================
# TOKEN INTELLIGENCE
# ============================================================

DEFAULT_TOKEN_BUDGET = 100000
MAX_CONTEXT_DOCUMENTS = 20

# ============================================================
# MEMORY
# ============================================================

MAX_MEMORY_RESULTS = 10

# ============================================================
# SECURITY
# ============================================================

MAX_COMMAND_LENGTH = 1000

# ============================================================
# LOGGING
# ============================================================

DEFAULT_LOG_LEVEL = "INFO"