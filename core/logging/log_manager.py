"""
File: core/logging/log_manager.py

Purpose:
Manage KAIROS log files.

Why:

Provides centralized
access to all log files.

Architecture:

KairosLogger
      ↓
LogManager
      ↓
LogConfig
      ↓
logs/
"""

from core.logging.log_config import LogConfig


class LogManager:
    """
    KAIROS Log Manager.
    """

    def __init__(
        self
    ):
        """
        Initialize manager.
        """

        LogConfig.create_log_directory()

    def get_log_file(
        self,
        log_name: str
    ) -> str:
        """
        Return log file path.

        Parameters:
            log_name:
                Logger name.

        Returns:
            Log file path.
        """

        log_map = {

            "kairos":
                str(
                    LogConfig.KAIROS_LOG
                ),

            "planner":
                str(
                    LogConfig.PLANNER_LOG
                ),

            "architect":
                str(
                    LogConfig.ARCHITECT_LOG
                ),
                
                
            "memory":
                str(
                    LogConfig.MEMORY_LOG
                ),

            "coder":
                str(
                    LogConfig.CODER_LOG
                ),

            "sandbox":
                str(
                    LogConfig.SANDBOX_LOG
                ),

            "reviewer":
                str(
                    LogConfig.REVIEWER_LOG
                ),

            "tester":
                str(
                    LogConfig.TESTER_LOG
                ),

            "healing":
                str(
                    LogConfig.HEALING_LOG
                )
            
            
        }

        return log_map.get(
            log_name.lower(),
            str(
                LogConfig.KAIROS_LOG
            )
        )