from dataclasses import dataclass


@dataclass
class ExecutionEngineConfig:
    max_retries: int = 3
    auto_repair: bool = True
    verify_after_execution: bool = True
    max_iterations: int = 10
    max_file_changes: int = 50
    enable_file_tools: bool = True
    enable_terminal: bool = True
    enable_web_search: bool = False
    enable_memory: bool = True
    enable_mcp: bool = False
