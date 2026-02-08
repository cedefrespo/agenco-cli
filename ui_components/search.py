"""
Search Menu UI
Functions for searching across all resources
"""

from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import box

from .common import console, COLORS, clear_screen, wait_for_key
from .display import print_info
from core import search_all, get_agent_content, get_context_content, get_prompt_content, copy_to_clipboard


def search_menu():
    """Search interface."""
    clear_screen()
    
    # Header
    panel = Panel(
        Text("SEARCH", style=f"bold {COLORS['search']}", justify="center"),
        box=box.ROUNDED,
        border_style=COLORS["search"],
        padding=(0, 2)
    )
    console.print(panel)
    console.print()
    
    query = Prompt.ask("Enter search query")
    
    if not query.strip():
        print_info("Search query cannot be empty.")
        wait_for_key()
        return
    
    results = search_all(query)
    total = sum(len(v) for v in results.values())
    
    console.print()
    
    if total == 0:
        print_info(f"No results found for '{query}'")
        wait_for_key()
        return
    
    console.print(f"[bold]Found {total} result{'s' if total != 1 else ''} for '[{COLORS['search']}]{query}[/]':[/]\n")
    
    # Agents results
    if results["agents"]:
        console.print(f"[{COLORS['agents']}]Agents ({len(results['agents'])}):[/]")
        for agent in results["agents"]:
            console.print(f"   - [{COLORS['agents']}]{agent['name']}[/] - {agent.get('description', '')}")
        console.print()
    
    # Contexts results
    if results["contexts"]:
        console.print(f"[{COLORS['contexts']}]Contexts ({len(results['contexts'])}):[/]")
        for ctx in results["contexts"]:
            console.print(f"   - [{COLORS['contexts']}]{ctx['name']}[/] - {ctx.get('description', '')}")
        console.print()
    
    # Prompts results
    if results["prompts"]:
        console.print(f"[{COLORS['prompts']}]Prompts ({len(results['prompts'])}):[/]")
        for prompt in results["prompts"]:
            console.print(f"   - [{COLORS['prompts']}]{prompt['name']}[/] - {prompt.get('description', '')}")
        console.print()
    
    # Quick actions
    console.print("[dim]Quick actions:[/]")
    console.print("  [1] Copy result to clipboard")
    console.print("  [0] Back to main menu")
    console.print()
    
    choice = Prompt.ask("Select option", default="0")
    
    if choice == "1":
        # Collect all names
        all_items = []
        for agent in results["agents"]:
            all_items.append(("agent", agent["name"]))
        for ctx in results["contexts"]:
            all_items.append(("context", ctx["name"]))
        for prompt in results["prompts"]:
            all_items.append(("prompt", prompt["name"]))
        
        if all_items:
            names = [f"{t}:{n}" for t, n in all_items]
            selected = Prompt.ask("Select item (type:name)", choices=names)
            item_type, item_name = selected.split(":", 1)
            
            content = None
            if item_type == "agent":
                content = get_agent_content(item_name)
            elif item_type == "context":
                content = get_context_content(item_name)
            elif item_type == "prompt":
                content = get_prompt_content(item_name)
            
            if content and copy_to_clipboard(content):
                from .display import print_success
                print_success(f"'{item_name}' copied to clipboard!")
            else:
                from .display import print_error
                print_error("Failed to copy to clipboard.")
            wait_for_key()
