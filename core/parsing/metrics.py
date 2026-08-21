"""
File: core/parsing/metrics.py

Purpose:
Track parser metrics for monitoring and debugging.

Why:
Understanding parser performance helps
optimize configurations and identify
problematic providers/models.

Architecture Position:

Structured Output Parser
    ↓
ParserMetrics
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime, UTC
import time


@dataclass
class ParserMetrics:
    """
    Metrics for structured output parsing.

    Tracks success rates, timing, and provider info
    without depending on ProviderManager.

    Attributes:
        provider: The LLM provider name.
        model: The model name.
        enabled: Whether metrics collection is enabled.
    """

    provider: str = "unknown"
    model: str = "unknown"
    enabled: bool = True

    # Counters
    _strict_success: int = 0
    _repair_success: int = 0
    _retry_success: int = 0
    _failure: int = 0
    _total_attempts: int = 0

    # Timing
    _parse_times: List[float] = field(default_factory=list)

    # History
    _history: List[Dict[str, Any]] = field(default_factory=list)

    def record_strict_success(self) -> None:
        """Record a strict parse success."""
        if not self.enabled:
            return
        self._strict_success += 1
        self._total_attempts += 1
        self._record_attempt("strict_success")

    def record_repair_success(self) -> None:
        """Record a repair parse success."""
        if not self.enabled:
            return
        self._repair_success += 1
        self._total_attempts += 1
        self._record_attempt("repair_success")

    def record_retry_success(self) -> None:
        """Record a retry parse success."""
        if not self.enabled:
            return
        self._retry_success += 1
        self._total_attempts += 1
        self._record_attempt("retry_success")

    def record_failure(self) -> None:
        """Record a parsing failure."""
        if not self.enabled:
            return
        self._failure += 1
        self._total_attempts += 1
        self._record_attempt("failure")

    def record_parse_time(self, time_ms: float) -> None:
        """
        Record a parse time.

        Args:
            time_ms: Parse time in milliseconds.
        """
        if not self.enabled:
            return
        self._parse_times.append(time_ms)

    def _record_attempt(self, result_type: str) -> None:
        """
        Record an attempt in history.

        Args:
            result_type: Type of result.
        """
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "result_type": result_type,
            "provider": self.provider,
            "model": self.model,
        }
        self._history.append(entry)

        # Keep only last 1000 entries
        if len(self._history) > 1000:
            self._history = self._history[-1000:]

    def get_success_rate(self) -> float:
        """
        Calculate overall success rate.

        Returns:
            Success rate as a float between 0 and 1.
        """
        if self._total_attempts == 0:
            return 0.0
        return (
            (self._strict_success + self._repair_success + self._retry_success)
            / self._total_attempts
        )

    def get_strict_success_rate(self) -> float:
        """Calculate strict success rate."""
        if self._total_attempts == 0:
            return 0.0
        return self._strict_success / self._total_attempts

    def get_repair_success_rate(self) -> float:
        """Calculate repair success rate."""
        if self._total_attempts == 0:
            return 0.0
        return self._repair_success / self._total_attempts

    def get_retry_success_rate(self) -> float:
        """Calculate retry success rate."""
        if self._total_attempts == 0:
            return 0.0
        return self._retry_success / self._total_attempts

    def get_failure_rate(self) -> float:
        """Calculate failure rate."""
        if self._total_attempts == 0:
            return 0.0
        return self._failure / self._total_attempts

    def get_average_parse_time_ms(self) -> float:
        """
        Calculate average parse time.

        Returns:
            Average parse time in milliseconds.
        """
        if not self._parse_times:
            return 0.0
        return sum(self._parse_times) / len(self._parse_times)

    def get_median_parse_time_ms(self) -> float:
        """Calculate median parse time."""
        if not self._parse_times:
            return 0.0
        sorted_times = sorted(self._parse_times)
        n = len(sorted_times)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_times[mid - 1] + sorted_times[mid]) / 2
        return sorted_times[mid]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metrics to dictionary.

        Returns:
            Dictionary of metrics.
        """
        return {
            "provider": self.provider,
            "model": self.model,
            "total_attempts": self._total_attempts,
            "strict_success": self._strict_success,
            "repair_success": self._repair_success,
            "retry_success": self._retry_success,
            "failure": self._failure,
            "success_rate": self.get_success_rate(),
            "strict_success_rate": self.get_strict_success_rate(),
            "repair_success_rate": self.get_repair_success_rate(),
            "retry_success_rate": self.get_retry_success_rate(),
            "failure_rate": self.get_failure_rate(),
            "average_parse_time_ms": self.get_average_parse_time_ms(),
            "median_parse_time_ms": self.get_median_parse_time_ms(),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self._strict_success = 0
        self._repair_success = 0
        self._retry_success = 0
        self._failure = 0
        self._total_attempts = 0
        self._parse_times = []
        self._history = []

    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent history entries.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            List of history entries.
        """
        return self._history[-limit:]

    def get_summary(self) -> str:
        """
        Get a human-readable summary.

        Returns:
            Summary string.
        """
        return (
            f"ParserMetrics[{self.provider}/{self.model}]: "
            f"{self._total_attempts} attempts, "
            f"{self.get_success_rate():.1%} success, "
            f"{self.get_average_parse_time_ms():.1f}ms avg"
        )