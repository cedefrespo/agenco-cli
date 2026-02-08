"""
Prompts Menu UI
Functions for displaying and managing prompts
"""

from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box

from .common import console, COLORS, clear_screen, wait_for_key
from .display import print_success, print_error, print_info
from core import (
    get_prompts, get_prompt, get_prompt_content,
    add_prompt, remove_prompt, copy_to_clipboard
)


def show_prompts_table():
    """Display prompts in a table."""
    prompts = get_prompts()
    
    if not prompts:
        print_info("No prompts found. Add one with option [3].")
        return
    
    table = Table(
        title="",
        box=box.ROUNDED,
        header_style=f"bold {COLORS['prompts']}",
        border_style=COLORS["prompts"],
        show_lines=True
    )
    
    table.add_column("Name", style=f"bold {COLORS['prompts']}", min_width=12)
    table.add_column("Description", style="white")
    table.add_column("Length", style="dim", justify="right")
    
    for prompt in prompts:
        prompt_len = len(prompt.get("prompt", ""))
        len_str = f"{prompt_len} chars"
        table.add_row(
            prompt.get("name", ""),
            prompt.get("description", "-"),
            len_str
        )
    
    console.print(table)


def show_prompt_details(name: str):
    """Show detailed view of a prompt."""
    prompt = get_prompt(name)
    if not prompt:
        print_error(f"Prompt '{name}' not found.")
        return
    
    # Header
    title = Text()
    title.append(prompt.get("name", ""), style=f"bold {COLORS['prompts']}")
    
    console.print(Panel(title, box=box.ROUNDED, border_style=COLORS["prompts"]))
    
    # Description
    console.print(f"\n[bold]Description:[/] {prompt.get('description', 'N/A')}")
    
    # Content
    content = prompt.get("prompt", "")
    console.print(f"\n[bold]Content:[/]")
    
    # Use Markdown rendering for the prompt
    md = Markdown(content)
    console.print(Panel(md, border_style="dim", padding=(1, 2)))


def prompts_menu():
    """Prompts submenu."""
    while True:
        clear_screen()
        
        # Header
        panel = Panel(
            Text("PROMPTS", style=f"bold {COLORS['prompts']}", justify="center"),
            box=box.ROUNDED,
            border_style=COLORS["prompts"],
            padding=(0, 2)
        )
        console.print(panel)
        console.print()
        
        # Show table
        show_prompts_table()
        console.print()
        
        # Menu options
        options = [
            "[1] Show prompt details",
            "[2] Copy prompt to clipboard",
            "[3] Add new prompt",
            "[4] Remove prompt",
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
            prompts = get_prompts()
            if prompts:
                names = [p["name"] for p in prompts]
                name = Prompt.ask(f"Prompt name", choices=names)
                clear_screen()
                show_prompt_details(name)
                wait_for_key()
        elif choice == "2":
            prompts = get_prompts()
            if prompts:
                names = [p["name"] for p in prompts]
                name = Prompt.ask(f"Prompt name", choices=names)
                content = get_prompt_content(name)
                if content is not None and copy_to_clipboard(content):
                    print_success(f"Prompt '{name}' copied to clipboard!")
                else:
                    print_error("Failed to copy to clipboard.")
                wait_for_key()
        elif choice == "3":
            name = Prompt.ask("Prompt name")
            description = Prompt.ask("Description", default="")
            console.print("[dim]Enter prompt content (end with empty line):[/]")
            lines = []
            while True:
                line = Prompt.ask("", default="")
                if line == "":
                    break
                lines.append(line)
            prompt_text = "\n".join(lines)
            if prompt_text:
                try:
                    add_prompt(name, description, prompt_text)
                    print_success(f"Prompt '{name}' added!")
                except ValueError as e:
                    print_error(str(e))
            else:
                print_error("Prompt content cannot be empty.")
            wait_for_key()
        elif choice == "4":
            prompts = get_prompts()
            if prompts:
                names = [p["name"] for p in prompts]
                name = Prompt.ask(f"Prompt name to remove", choices=names)
                if Confirm.ask(f"[{COLORS['warning']}]Are you sure you want to remove '{name}'?[/]"):
                    if remove_prompt(name):
                        print_success(f"Prompt '{name}' removed!")
                    else:
                        print_error(f"Failed to remove prompt.")
                wait_for_key()
