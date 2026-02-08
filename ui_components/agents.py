"""
Agents Menu UI
Functions for displaying and managing agents
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
    get_agents, get_agent, get_agent_content,
    add_agent, remove_agent, copy_to_clipboard
)


def show_agents_table():
    """Display agents in a table."""
    agents = get_agents()
    
    if not agents:
        print_info("No agents found. Add one with option [3].")
        return
    
    table = Table(
        title="",
        box=box.ROUNDED,
        header_style=f"bold {COLORS['agents']}",
        border_style=COLORS["agents"],
        show_lines=True
    )
    
    table.add_column("Name", style=f"bold {COLORS['agents']}", min_width=12)
    table.add_column("Description", style="white")
    table.add_column("Files", style="dim")
    
    for agent in agents:
        files_count = len(agent.get("files", []))
        files_str = f"{files_count} file{'s' if files_count != 1 else ''}"
        table.add_row(
            agent.get("name", ""),
            agent.get("description", "-"),
            files_str
        )
    
    console.print(table)


def show_agent_details(name: str):
    """Show detailed view of an agent."""
    agent = get_agent(name)
    if not agent:
        print_error(f"Agent '{name}' not found.")
        return
    
    # Header
    title = Text()
    title.append(agent.get("name", ""), style=f"bold {COLORS['agents']}")
    
    console.print(Panel(title, box=box.ROUNDED, border_style=COLORS["agents"]))
    
    # Description
    console.print(f"\n[bold]Description:[/] {agent.get('description', 'N/A')}")
    
    # Files
    console.print(f"\n[bold]Files:[/]")
    for f in agent.get("files", []):
        console.print(f"  [dim]•[/] {f}")
    
    # Content preview
    content = get_agent_content(name)
    if content:
        console.print(f"\n[bold]Content Preview:[/]")
        preview = content[:500] + ("..." if len(content) > 500 else "")
        syntax = Syntax(preview, "markdown", theme="monokai", line_numbers=False)
        console.print(Panel(syntax, border_style="dim"))


def agents_menu():
    """Agents submenu."""
    while True:
        clear_screen()
        
        # Header
        panel = Panel(
            Text("AGENTS", style=f"bold {COLORS['agents']}", justify="center"),
            box=box.ROUNDED,
            border_style=COLORS["agents"],
            padding=(0, 2)
        )
        console.print(panel)
        console.print()
        
        # Show table
        show_agents_table()
        console.print()
        
        # Menu options
        options = [
            "[1] Show agent details",
            "[2] Copy agent to clipboard",
            "[3] Add new agent",
            "[4] Remove agent",
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
            agents = get_agents()
            if agents:
                names = [a["name"] for a in agents]
                name = Prompt.ask(f"Agent name", choices=names)
                clear_screen()
                show_agent_details(name)
                wait_for_key()
        elif choice == "2":
            agents = get_agents()
            if agents:
                names = [a["name"] for a in agents]
                name = Prompt.ask(f"Agent name", choices=names)
                content = get_agent_content(name)
                if content and copy_to_clipboard(content):
                    print_success(f"Agent '{name}' copied to clipboard!")
                else:
                    print_error("Failed to copy to clipboard.")
                wait_for_key()
        elif choice == "3":
            name = Prompt.ask("Agent name")
            description = Prompt.ask("Description", default="")
            files_input = Prompt.ask("Files (comma-separated paths)")
            files = [f.strip() for f in files_input.split(",") if f.strip()]
            try:
                add_agent(name, description, files)
                print_success(f"Agent '{name}' added!")
            except ValueError as e:
                print_error(str(e))
            wait_for_key()
        elif choice == "4":
            agents = get_agents()
            if agents:
                names = [a["name"] for a in agents]
                name = Prompt.ask(f"Agent name to remove", choices=names)
                if Confirm.ask(f"[{COLORS['warning']}]Are you sure you want to remove '{name}'?[/]"):
                    if remove_agent(name):
                        print_success(f"Agent '{name}' removed!")
                    else:
                        print_error(f"Failed to remove agent.")
                wait_for_key()
