"""
UI Display Functions
Functions for printing headers, messages, and stats
"""

from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich import box

from .common import console, COLORS, VERSION
from core import get_stats


def print_header():
    """Print the main header."""
    header = Text()
    header.append("AGENCO CLI", style="bold white")
    header.append(f" v{VERSION}", style="dim")
    
    subtitle = Text("Manage Agents, Contexts & Prompts", style="dim italic")
    
    panel = Panel(
        Align.center(header + "\n" + subtitle),
        box=box.ROUNDED,
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)


def print_stats():
    """Print statistics bar."""
    stats = get_stats()
    
    stats_text = Text()
    stats_text.append("Stats: ", style="bold")
    stats_text.append(f"{stats['agents']} agents", style=COLORS["agents"])
    stats_text.append(" | ", style="dim")
    stats_text.append(f"{stats['contexts']} contexts", style=COLORS["contexts"])
    stats_text.append(" | ", style="dim")
    stats_text.append(f"{stats['prompts']} prompts", style=COLORS["prompts"])
    
    console.print(Align.center(stats_text))
    console.print()


def print_success(message: str):
    """Print success message."""
    console.print(f"[{COLORS['success']}]{message}[/]")


def print_error(message: str):
    """Print error message."""
    console.print(f"[{COLORS['error']}]{message}[/]")


def print_info(message: str):
    """Print info message."""
    console.print(f"[{COLORS['info']}]{message}[/]")
