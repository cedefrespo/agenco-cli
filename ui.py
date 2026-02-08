"""
Agenco CLI - Interactive UI
Beautiful terminal interface using Rich library.
"""

import sys
from typing import Optional, Callable

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.markdown import Markdown
from rich import box

from core import (
    get_agents, get_agent, get_agent_content, add_agent, remove_agent,
    get_contexts, get_context, get_context_content, add_context, remove_context,
    get_prompts, get_prompt, get_prompt_content, add_prompt, remove_prompt,
    copy_to_clipboard, search_all, get_stats
)

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


def wait_for_key():
    """Wait for user to press Enter."""
    console.print()
    Prompt.ask("[dim]Press Enter to continue[/]", default="")


def create_menu(title: str, options: list, color: str = "blue") -> str:
    """Create and display a menu, return selected option."""
    panel = Panel(
        Align.center(Text(title, style=f"bold {color}")),
        box=box.ROUNDED,
        border_style=color,
        padding=(0, 2)
    )
    console.print(panel)
    console.print()
    
    for opt in options:
        key = opt.get("key", "")
        label = opt.get("label", "")
        icon = opt.get("icon", "")
        style = opt.get("style", "")
        
        if key == "":
            console.print(f"  {icon} {label}", style=style)
        else:
            console.print(f"  [{COLORS['info']}][{key}][/] {icon} {label}", style=style)
    
    console.print()
    choice = Prompt.ask("Select option", default="0")
    return choice


# ============================================
# AGENTS UI
# ============================================

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
            Align.center(Text("AGENTS", style=f"bold {COLORS['agents']}")),
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
            {"key": "1", "label": "Show agent details"},
            {"key": "2", "label": "Copy agent to clipboard"},
            {"key": "3", "label": "Add new agent"},
            {"key": "4", "label": "Remove agent"},
            {"key": "", "label": ""},
            {"key": "0", "label": "Back to main menu"},
        ]
        
        for opt in options:
            if opt["key"]:
                console.print(f"  [{COLORS['info']}][{opt['key']}][/] {opt['label']}")
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


# ============================================
# CONTEXTS UI
# ============================================

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
            Align.center(Text("CONTEXTS", style=f"bold {COLORS['contexts']}")),
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
            {"key": "1", "label": "Show context details"},
            {"key": "2", "label": "Copy context to clipboard"},
            {"key": "3", "label": "Add new context"},
            {"key": "4", "label": "Remove context"},
            {"key": "", "label": ""},
            {"key": "0", "label": "Back to main menu"},
        ]
        
        for opt in options:
            if opt["key"]:
                console.print(f"  [{COLORS['info']}][{opt['key']}][/] {opt['label']}")
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


# ============================================
# PROMPTS UI
# ============================================

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
            Align.center(Text("PROMPTS", style=f"bold {COLORS['prompts']}")),
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
            {"key": "1", "label": "Show prompt details"},
            {"key": "2", "label": "Copy prompt to clipboard"},
            {"key": "3", "label": "Add new prompt"},
            {"key": "4", "label": "Remove prompt"},
            {"key": "", "label": ""},
            {"key": "0", "label": "Back to main menu"},
        ]
        
        for opt in options:
            if opt["key"]:
                console.print(f"  [{COLORS['info']}][{opt['key']}][/] {opt['label']}")
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


# ============================================
# SEARCH UI
# ============================================

def search_menu():
    """Search interface."""
    clear_screen()
    
    # Header
    panel = Panel(
        Align.center(Text("SEARCH", style=f"bold {COLORS['search']}")),
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
                print_success(f"'{item_name}' copied to clipboard!")
            else:
                print_error("Failed to copy to clipboard.")
            wait_for_key()


# ============================================
# MAIN MENU
# ============================================

def main_menu():
    """Main menu loop."""
    while True:
        clear_screen()
        print_header()
        console.print()
        print_stats()
        
        # Menu options
        console.print(f"  [{COLORS['info']}][1][/] Agents")
        console.print(f"  [{COLORS['info']}][2][/] Contexts")
        console.print(f"  [{COLORS['info']}][3][/] Prompts")
        console.print(f"  [{COLORS['info']}][4][/] Search")
        console.print()
        console.print(f"  [{COLORS['info']}][5][/] Exit")
        
        console.print()
        choice = Prompt.ask("Select option", default="5")
        
        if choice == "1":
            agents_menu()
        elif choice == "2":
            contexts_menu()
        elif choice == "3":
            prompts_menu()
        elif choice == "4":
            search_menu()
        elif choice == "5" or choice.lower() in ["q", "quit", "exit"]:
            clear_screen()
            console.print(Panel(
                Align.center(Text("Goodbye!", style="bold blue")),
                box=box.ROUNDED,
                border_style="blue",
                padding=(0, 2)
            ))
            break


def run_interactive():
    """Entry point for interactive mode."""
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n")
        console.print("[dim]Interrupted. Goodbye![/]")
        sys.exit(0)


if __name__ == "__main__":
    run_interactive()
