

class TerminalVisualization:

    def __init__(self) -> None:
        """Initialize terminal color mappings for visualization output."""
        self.COLORS = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "reset": "\033[0m"
        }

    def colorize(self, text: str, color: str) -> str:
        """Wrap text with ANSI color escape codes for terminal output."""
        code = self.COLORS.get(color.lower(), "")
        return f"{code}{text}{self.COLORS['reset']}" if code else text
