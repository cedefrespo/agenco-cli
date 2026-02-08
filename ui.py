"""
Agenco CLI - Interactive UI
Main entry point for the interactive interface
"""

import sys
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

from ui_components import (
    console,
    COLORS,
    clear_screen,
    print_header,
    print_stats,
    agents_menu,
    contexts_menu,
    prompts_menu,
    search_menu,
    publish_menu
)


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
        console.print(f"  [{COLORS['info']}][5][/] Publish to Marketplace")
        console.print()
        console.print(f"  [{COLORS['info']}][0][/] Exit")
        
        console.print()
        choice = Prompt.ask("Select option", default="0")
        
        if choice == "1":
            agents_menu()
        elif choice == "2":
            contexts_menu()
        elif choice == "3":
            prompts_menu()
        elif choice == "4":
            search_menu()
        elif choice == "5":
            publish_menu()
        elif choice == "0" or choice.lower() in ["q", "quit", "exit"]:
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
