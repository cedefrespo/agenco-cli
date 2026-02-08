"""
UI Components - Publish Menu
Handles publishing resources to Agenco marketplace
"""

import os
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

from .common import console, COLORS, clear_screen, wait_for_key
from .display import print_header, print_success, print_error, print_info

from core import (
    get_agents,
    get_contexts,
    get_prompts,
    publish_agent,
    publish_context,
    publish_prompt
)


def publish_menu():
    """Publish menu - select resource type and publish to marketplace."""
    while True:
        clear_screen()
        print_header()
        console.print()
        console.print(f"[{COLORS['title']}]Publish to Marketplace[/]", style="bold")
        console.print()
        
        # Menu options
        console.print(f"  [{COLORS['info']}][1][/] Publish Agent")
        console.print(f"  [{COLORS['info']}][2][/] Publish Context")
        console.print(f"  [{COLORS['info']}][3][/] Publish Prompt")
        console.print()
        console.print(f"  [{COLORS['info']}][0][/] Back to main menu")
        
        console.print()
        choice = Prompt.ask("Select option", default="0")
        
        if choice == "1":
            publish_agent_interactive()
        elif choice == "2":
            publish_context_interactive()
        elif choice == "3":
            publish_prompt_interactive()
        elif choice == "0":
            break


def publish_agent_interactive():
    """Interactive agent publishing."""
    clear_screen()
    print_header()
    console.print()
    console.print(f"[{COLORS['title']}]Publish Agent[/]", style="bold")
    console.print()
    
    # Show available agents
    agents = get_agents()
    if not agents:
        print_error("No agents found. Create an agent first.")
        wait_for_key()
        return
    
    console.print(f"[{COLORS['secondary']}]Available Agents:[/]")
    for i, agent in enumerate(agents, 1):
        console.print(f"  [{COLORS['info']}]{i}.[/] {agent['name']}")
    console.print()
    
    # Select agent
    choice = Prompt.ask("Select agent number (or press Enter to cancel)", default="")
    if not choice or not choice.isdigit():
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(agents):
        print_error("Invalid selection")
        wait_for_key()
        return
    
    agent_name = agents[idx]['name']
    
    # Get authentication
    token = os.getenv("AGENCO_TOKEN")
    if not token:
        console.print()
        console.print(f"[{COLORS['warning']}]Authentication required.[/]")
        console.print(f"Set AGENCO_TOKEN environment variable or enter token now.")
        console.print()
        token = Prompt.ask("API Token (press Enter to cancel)", default="")
        if not token:
            return
    
    # Get API URL
    api_url = os.getenv("AGENCO_API_URL", "https://api.agenco.dev")
    use_custom_url = Prompt.ask(
        f"Use custom API URL? (current: {api_url})",
        choices=["y", "n"],
        default="n"
    )
    if use_custom_url == "y":
        api_url = Prompt.ask("API URL", default=api_url)
    
    # Publish
    console.print()
    console.print(f"[{COLORS['info']}]Publishing agent '{agent_name}' to marketplace...[/]")
    
    try:
        result = publish_agent(agent_name, api_url=api_url, token=token)
        console.print()
        print_success(f"Successfully published '{agent_name}'!")
        if result.get("id"):
            console.print(f"  [{COLORS['secondary']}]ID:[/] {result['id']}")
        if result.get("url"):
            console.print(f"  [{COLORS['secondary']}]URL:[/] {result['url']}")
        if result.get("action"):
            action = result['action']
            console.print(f"  [{COLORS['secondary']}]Action:[/] {action}")
    except Exception as e:
        console.print()
        print_error(f"Failed to publish: {str(e)}")
    
    console.print()
    wait_for_key()


def publish_context_interactive():
    """Interactive context publishing."""
    clear_screen()
    print_header()
    console.print()
    console.print(f"[{COLORS['title']}]Publish Context[/]", style="bold")
    console.print()
    
    # Show available contexts
    contexts = get_contexts()
    if not contexts:
        print_error("No contexts found. Create a context first.")
        wait_for_key()
        return
    
    console.print(f"[{COLORS['secondary']}]Available Contexts:[/]")
    for i, ctx in enumerate(contexts, 1):
        console.print(f"  [{COLORS['info']}]{i}.[/] {ctx['name']}")
    console.print()
    
    # Select context
    choice = Prompt.ask("Select context number (or press Enter to cancel)", default="")
    if not choice or not choice.isdigit():
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(contexts):
        print_error("Invalid selection")
        wait_for_key()
        return
    
    context_name = contexts[idx]['name']
    
    # Get authentication
    token = os.getenv("AGENCO_TOKEN")
    if not token:
        console.print()
        console.print(f"[{COLORS['warning']}]Authentication required.[/]")
        console.print(f"Set AGENCO_TOKEN environment variable or enter token now.")
        console.print()
        token = Prompt.ask("API Token (press Enter to cancel)", default="")
        if not token:
            return
    
    # Get API URL
    api_url = os.getenv("AGENCO_API_URL", "https://api.agenco.dev")
    use_custom_url = Prompt.ask(
        f"Use custom API URL? (current: {api_url})",
        choices=["y", "n"],
        default="n"
    )
    if use_custom_url == "y":
        api_url = Prompt.ask("API URL", default=api_url)
    
    # Publish
    console.print()
    console.print(f"[{COLORS['info']}]Publishing context '{context_name}' to marketplace...[/]")
    
    try:
        result = publish_context(context_name, api_url=api_url, token=token)
        console.print()
        print_success(f"Successfully published '{context_name}'!")
        if result.get("id"):
            console.print(f"  [{COLORS['secondary']}]ID:[/] {result['id']}")
        if result.get("url"):
            console.print(f"  [{COLORS['secondary']}]URL:[/] {result['url']}")
        if result.get("action"):
            action = result['action']
            console.print(f"  [{COLORS['secondary']}]Action:[/] {action}")
    except Exception as e:
        console.print()
        print_error(f"Failed to publish: {str(e)}")
    
    console.print()
    wait_for_key()


def publish_prompt_interactive():
    """Interactive prompt publishing."""
    clear_screen()
    print_header()
    console.print()
    console.print(f"[{COLORS['title']}]Publish Prompt[/]", style="bold")
    console.print()
    
    # Show available prompts
    prompts = get_prompts()
    if not prompts:
        print_error("No prompts found. Create a prompt first.")
        wait_for_key()
        return
    
    console.print(f"[{COLORS['secondary']}]Available Prompts:[/]")
    for i, prompt in enumerate(prompts, 1):
        console.print(f"  [{COLORS['info']}]{i}.[/] {prompt['name']}")
    console.print()
    
    # Select prompt
    choice = Prompt.ask("Select prompt number (or press Enter to cancel)", default="")
    if not choice or not choice.isdigit():
        return
    
    idx = int(choice) - 1
    if idx < 0 or idx >= len(prompts):
        print_error("Invalid selection")
        wait_for_key()
        return
    
    prompt_name = prompts[idx]['name']
    
    # Get authentication
    token = os.getenv("AGENCO_TOKEN")
    if not token:
        console.print()
        console.print(f"[{COLORS['warning']}]Authentication required.[/]")
        console.print(f"Set AGENCO_TOKEN environment variable or enter token now.")
        console.print()
        token = Prompt.ask("API Token (press Enter to cancel)", default="")
        if not token:
            return
    
    # Get API URL
    api_url = os.getenv("AGENCO_API_URL", "https://api.agenco.dev")
    use_custom_url = Prompt.ask(
        f"Use custom API URL? (current: {api_url})",
        choices=["y", "n"],
        default="n"
    )
    if use_custom_url == "y":
        api_url = Prompt.ask("API URL", default=api_url)
    
    # Publish
    console.print()
    console.print(f"[{COLORS['info']}]Publishing prompt '{prompt_name}' to marketplace...[/]")
    
    try:
        result = publish_prompt(prompt_name, api_url=api_url, token=token)
        console.print()
        print_success(f"Successfully published '{prompt_name}'!")
        if result.get("id"):
            console.print(f"  [{COLORS['secondary']}]ID:[/] {result['id']}")
        if result.get("url"):
            console.print(f"  [{COLORS['secondary']}]URL:[/] {result['url']}")
        if result.get("action"):
            action = result['action']
            console.print(f"  [{COLORS['secondary']}]Action:[/] {action}")
    except Exception as e:
        console.print()
        print_error(f"Failed to publish: {str(e)}")
    
    console.print()
    wait_for_key()
