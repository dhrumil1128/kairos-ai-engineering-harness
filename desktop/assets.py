"""
Asset resolution for development and PyInstaller builds.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from desktop.utils import RuntimeEnvironment, get_runtime_environment


@dataclass(frozen=True)
class AssetResolver:
    """
    Resolve desktop assets in both source and frozen layouts.
    """

    environment: RuntimeEnvironment

    def path(self, name: str) -> Path | None:
        """
        Return the first existing path for an asset name.
        """

        for root in self.roots():
            candidate = root / name

            if candidate.exists():
                return candidate.resolve()

        return None

    def require(self, name: str) -> Path:
        """
        Return an asset path or raise a clear error.
        """

        asset_path = self.path(name)

        if asset_path is None:
            raise FileNotFoundError(f"Missing desktop asset: {name}")

        return asset_path

    def roots(self) -> list[Path]:
        """
        Candidate asset roots ordered by runtime likelihood.
        """

        roots: list[Path] = []

        if self.environment.bundled_root:
            roots.append(self.environment.bundled_root / "assets")
            roots.append(self.environment.bundled_root / "packaging" / "assets")

        roots.extend(
            [
                self.environment.executable_dir / "assets",
                self.environment.executable_dir / "packaging" / "assets",
                self.environment.project_root / "packaging" / "assets",
            ]
        )

        return roots


def get_asset_path(
    name: str,
    environment: RuntimeEnvironment | None = None,
) -> Path | None:
    """
    Convenience wrapper for resolving one asset.
    """

    return AssetResolver(environment or get_runtime_environment()).path(name)
