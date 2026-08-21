"""
Asset resolution for the KAIROS launcher.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from launcher.utils import RuntimeEnvironment, get_runtime_environment


@dataclass(frozen=True)
class AssetLocator:
    """
    Resolve launcher asset paths for development and PyInstaller modes.
    """

    environment: RuntimeEnvironment

    def get_asset_path(
        self,
        name: str,
    ) -> Path | None:
        """
        Return the first existing asset path for the requested asset.
        """

        for base_path in self._asset_roots():
            asset_path = base_path / name

            if asset_path.exists():
                return asset_path

        return None

    def _asset_roots(self) -> list[Path]:
        roots: list[Path] = []

        if self.environment.bundled_root:
            roots.append(self.environment.bundled_root / "assets")
            roots.append(self.environment.bundled_root / "packaging" / "assets")

        roots.append(self.environment.executable_dir / "assets")
        roots.append(self.environment.executable_dir / "packaging" / "assets")
        roots.append(self.environment.project_root / "packaging" / "assets")

        return roots


def get_asset_path(
    name: str,
    environment: RuntimeEnvironment | None = None,
) -> Path | None:
    """
    Convenience function for resolving packaged assets.
    """

    locator = AssetLocator(
        environment or get_runtime_environment()
    )

    return locator.get_asset_path(name)
