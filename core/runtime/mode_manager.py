class ModeManager:
    """
    Manage the current KAIROS operating mode.
    """

    GENERATION = "generation"
    DESKTOP = "desktop"

    def __init__(self):
        # Default mode
        self._mode = self.GENERATION

    def get_mode(self) -> str:
        """Return the current mode."""
        return self._mode

    def set_mode(self, mode: str) -> bool:
        """
        Set the active mode.

        Returns:
            True if the mode was changed successfully.
            False if the mode is invalid.
        """
        mode = mode.lower()

        if mode not in (self.GENERATION, self.DESKTOP):
            return False

        self._mode = mode
        return True

    def is_generation(self) -> bool:
        """Check if Generation Mode is active."""
        return self._mode == self.GENERATION

    def is_desktop(self) -> bool:
        """Check if Desktop Automation Mode is active."""
        return self._mode == self.DESKTOP