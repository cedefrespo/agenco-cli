"""
Contexts Menu UI
Functions for displaying and managing contexts
"""

from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box

from .common import console, COLORS, clear_screen, wait_for_key
from .display import print_success, print_error, print_info
from core import (
    get_contexts, get_context, get_context_content,
    add_context, remove_context, copy_to_clipboard
)


def show_contexts_table():
    """Display contexts in a table."""
    contexts = get_contexts()
    
    if not contexts:
        print_info("No contexts found. Add one with option [3].")
        return
    
    table = Table(
        title="",
        box=box.ROUNDED,
        header_style=f"bold {COLORS['contexts']}",
        border_style=COLORS["contexts"],
        show_lines=True
    )
    
    table.add_column("Name", style=f"bold {COLORS['contexts']}", min_width=12)
    table.add_column("Description", style="white")
    table.add_column("Files", style="dim")
    
    for ctx in contexts:
        files_count = len(ctx.get("files", []))
        files_str = f"{files_count} file{'s' if files_count != 1 else ''}"
        table.add_row(
            ctx.get("name", ""),
            ctx.get("description", "-"),
            files_str
        )
    
    console.print(table)


def show_context_details(name: str):
    """Show detailed view of a context."""
    ctx = get_context(name)
    if not ctx:
        print_error(f"Context '{name}' not found.")
        return
    
    # Header
    title = Text()
    title.append(ctx.get("name", ""), style=f"bold {COLORS['contexts']}")
    
    console.print(Panel(title, box=box.ROUNDED, border_style=COLORS["contexts"]))
    
    # Description
    console.print(f"\n[bold]Description:[/] {ctx.get('description', 'N/A')}")
    
    # Files
    console.print(f"\n[bold]Files:[/]")
    for f in ctx.get("files", []):
        console.print(f"  [dim]•[/] {f}")
    
    # Content preview
    content = get_context_content(name)
    if content:
        console.print(f"\n[bold]Content Preview:[/]")
        preview = content[:500] + ("..." if len(content) > 500 else "")
        syntax = Syntax(preview, "markdown", theme="monokai", line_numbers=False)
        console.print(Panel(syntax, border_style="dim"))


def contexts_menu():
    """Contexts submenu."""
    while True:
        clear_screen()
        
        # Header
        panel = Panel(
            Text("CONTEXTS", style=f"bold {COLORS['contexts']}", justify="center"),
            box=box.ROUNDED,
            border_style=COLORS["contexts"],
            padding=(0, 2)
        )
        console.print(panel)
        console.print()
        
        # Show table
        show_contexts_table()
        console.print()
        
        # Menu options
        options = [
            "[1] Show context details",
            "[2] Copy context to clipboard",
            "[3] Add new context",
            "[4] Remove context",
            "",
            "[0] Back to main menu",
        ]
        
        for opt in options:
            if opt:
                console.print(f"  [{COLORS['info']}]{opt}[/]")
            else:
                console.print()
        
        console.print()
        choice = Prompt.ask("Select option", default="0")
        
        if choice == "0":
            break
        elif choice == "1":
            contexts = get_contexts()
            if contexts:
                names = [c["name"] for c in contexts]
                name = Prompt.ask(f"Context name", choices=names)
                clear_screen()
                show_context_details(name)
                wait_for_key()
        elif choice == "2":
            contexts = get_contexts()
            if contexts:
                names = [c["name"] for c in contexts]
                name = Prompt.ask(f"Context name", choices=names)
                content = get_context_content(name)
                if content and copy_to_clipboard(content):
                    print_success(f"Context '{name}' copied to clipboard!")
                else:
                    print_error("Failed to copy to clipboard.")
                wait_for_key()
        elif choice == "3":
            name = Prompt.ask("Context name")
            description = Prompt.ask("Description", default="")
            files_input = Prompt.ask("Files (comma-separated paths)")
            files = [f.strip() for f in files_input.split(",") if f.strip()]
            try:
                add_context(name, description, files)
                print_success(f"Context '{name}' added!")
            except ValueError as e:
                print_error(str(e))
            wait_for_key()
        elif choice == "4":
            contexts = get_contexts()
            if contexts:
                names = [c["name"] for c in contexts]
                name = Prompt.ask(f"Context name to remove", choices=names)
                if Confirm.ask(f"[{COLORS['warning']}]Are you sure you want to remove '{name}'?[/]"):
                    if remove_context(name):
                        print_success(f"Context '{name}' removed!")
                    else:
                        print_error(f"Failed to remove context.")
                wait_for_key()
