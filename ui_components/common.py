"""
UI Constants and Utilities
Shared configuration for the CLI interface
"""

from rich.console import Console

# Initialize console
console = Console()

# Colors for each section
COLORS = {
    "agents": "cyan",
    "contexts": "green", 
    "prompts": "yellow",
    "search": "magenta",
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "muted": "dim white",
}

VERSION = "1.0"


def clear_screen():
    """Clear the terminal screen."""
    console.clear()


def wait_for_key():
    """Wait for user to press Enter."""
    from rich.prompt import Prompt
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/]", default="")
