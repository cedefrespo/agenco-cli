"""
Agenco CLI - Core Logic
Manages agents, contexts, and prompts from JSON files.
"""

import json
import os
from pathlib import Path
from typing import Optional

# Base directory for config files
BASE_DIR = Path(__file__).parent
AGENTS_FILE = BASE_DIR / "agents.json"
CONTEXTS_FILE = BASE_DIR / "contexts.json"
PROMPTS_FILE = BASE_DIR / "prompts.json"


def expand_path(path: str) -> Path:
    """Expand ~ and environment variables in path."""
    return Path(os.path.expanduser(os.path.expandvars(path)))


def load_json(filepath: Path) -> dict:
    """Load JSON file, return empty dict if not found."""
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath: Path, data: dict) -> None:
    """Save data to JSON file with pretty formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================
# AGENTS
# ============================================

def get_agents() -> list:
    """Get all agents."""
    data = load_json(AGENTS_FILE)
    return data.get("agents", [])


def get_agent(name: str) -> Optional[dict]:
    """Get agent by name."""
    agents = get_agents()
    for agent in agents:
        if agent.get("name") == name:
            return agent
    return None


def add_agent(name: str, description: str, files: list) -> dict:
    """Add a new agent."""
    data = load_json(AGENTS_FILE)
    if "agents" not in data:
        data["agents"] = []
    
    # Check if agent already exists
    for agent in data["agents"]:
        if agent.get("name") == name:
            raise ValueError(f"Agent '{name}' already exists")
    
    new_agent = {
        "name": name,
        "description": description,
        "files": files
    }
    data["agents"].append(new_agent)
    save_json(AGENTS_FILE, data)
    return new_agent


def remove_agent(name: str) -> bool:
    """Remove an agent by name."""
    data = load_json(AGENTS_FILE)
    agents = data.get("agents", [])
    
    for i, agent in enumerate(agents):
        if agent.get("name") == name:
            del agents[i]
            save_json(AGENTS_FILE, data)
            return True
    return False


def get_agent_content(name: str) -> Optional[str]:
    """Get the content of all files for an agent."""
    agent = get_agent(name)
    if not agent:
        return None
    
    content_parts = []
    for file_path in agent.get("files", []):
        expanded = expand_path(file_path)
        if expanded.exists():
            with open(expanded, 'r', encoding='utf-8') as f:
                content_parts.append(f"# File: {file_path}\n\n{f.read()}")
        else:
            content_parts.append(f"# File: {file_path}\n\n[FILE NOT FOUND]")
    
    return "\n\n---\n\n".join(content_parts)


# ============================================
# CONTEXTS
# ============================================

def get_contexts() -> list:
    """Get all contexts."""
    data = load_json(CONTEXTS_FILE)
    return data.get("contexts", [])


def get_context(name: str) -> Optional[dict]:
    """Get context by name."""
    contexts = get_contexts()
    for ctx in contexts:
        if ctx.get("name") == name:
            return ctx
    return None


def add_context(name: str, description: str, files: list) -> dict:
    """Add a new context."""
    data = load_json(CONTEXTS_FILE)
    if "contexts" not in data:
        data["contexts"] = []
    
    # Check if context already exists
    for ctx in data["contexts"]:
        if ctx.get("name") == name:
            raise ValueError(f"Context '{name}' already exists")
    
    new_context = {
        "name": name,
        "description": description,
        "files": files
    }
    data["contexts"].append(new_context)
    save_json(CONTEXTS_FILE, data)
    return new_context


def remove_context(name: str) -> bool:
    """Remove a context by name."""
    data = load_json(CONTEXTS_FILE)
    contexts = data.get("contexts", [])
    
    for i, ctx in enumerate(contexts):
        if ctx.get("name") == name:
            del contexts[i]
            save_json(CONTEXTS_FILE, data)
            return True
    return False


def get_context_content(name: str) -> Optional[str]:
    """Get the content of all files for a context."""
    ctx = get_context(name)
    if not ctx:
        return None
    
    content_parts = []
    for file_path in ctx.get("files", []):
        expanded = expand_path(file_path)
        if expanded.exists():
            with open(expanded, 'r', encoding='utf-8') as f:
                content_parts.append(f"# File: {file_path}\n\n{f.read()}")
        else:
            content_parts.append(f"# File: {file_path}\n\n[FILE NOT FOUND]")
    
    return "\n\n---\n\n".join(content_parts)


# ============================================
# PROMPTS
# ============================================

def get_prompts() -> list:
    """Get all prompts."""
    data = load_json(PROMPTS_FILE)
    return data.get("prompts", [])


def get_prompt(name: str) -> Optional[dict]:
    """Get prompt by name."""
    prompts = get_prompts()
    for prompt in prompts:
        if prompt.get("name") == name:
            return prompt
    return None


def add_prompt(name: str, description: str, prompt_text: str) -> dict:
    """Add a new prompt."""
    data = load_json(PROMPTS_FILE)
    if "prompts" not in data:
        data["prompts"] = []
    
    # Check if prompt already exists
    for p in data["prompts"]:
        if p.get("name") == name:
            raise ValueError(f"Prompt '{name}' already exists")
    
    new_prompt = {
        "name": name,
        "description": description,
        "prompt": prompt_text
    }
    data["prompts"].append(new_prompt)
    save_json(PROMPTS_FILE, data)
    return new_prompt


def update_prompt(name: str, description: Optional[str] = None, prompt_text: Optional[str] = None) -> Optional[dict]:
    """Update an existing prompt."""
    data = load_json(PROMPTS_FILE)
    prompts = data.get("prompts", [])
    
    for prompt in prompts:
        if prompt.get("name") == name:
            if description is not None:
                prompt["description"] = description
            if prompt_text is not None:
                prompt["prompt"] = prompt_text
            save_json(PROMPTS_FILE, data)
            return prompt
    return None


def remove_prompt(name: str) -> bool:
    """Remove a prompt by name."""
    data = load_json(PROMPTS_FILE)
    prompts = data.get("prompts", [])
    
    for i, prompt in enumerate(prompts):
        if prompt.get("name") == name:
            del prompts[i]
            save_json(PROMPTS_FILE, data)
            return True
    return False


def get_prompt_content(name: str) -> Optional[str]:
    """Get the prompt text for a prompt."""
    prompt = get_prompt(name)
    if not prompt:
        return None
    return prompt.get("prompt", "")


# ============================================
# CLIPBOARD UTILITIES
# ============================================

def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard."""
    import subprocess
    import sys
    
    try:
        if sys.platform == "darwin":  # macOS
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return process.returncode == 0
        elif sys.platform == "linux":
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return process.returncode == 0
        elif sys.platform == "win32":
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            process.communicate(text.encode('utf-8'))
            return process.returncode == 0
    except Exception:
        pass
    return False


# ============================================
# SEARCH
# ============================================

def search_all(query: str) -> dict:
    """Search across agents, contexts, and prompts."""
    query = query.lower()
    results = {
        "agents": [],
        "contexts": [],
        "prompts": []
    }
    
    for agent in get_agents():
        if query in agent.get("name", "").lower() or query in agent.get("description", "").lower():
            results["agents"].append(agent)
    
    for ctx in get_contexts():
        if query in ctx.get("name", "").lower() or query in ctx.get("description", "").lower():
            results["contexts"].append(ctx)
    
    for prompt in get_prompts():
        if (query in prompt.get("name", "").lower() or 
            query in prompt.get("description", "").lower() or
            query in prompt.get("prompt", "").lower()):
            results["prompts"].append(prompt)
    
    return results


# ============================================
# STATS
# ============================================

def get_stats() -> dict:
    """Get statistics about the registry."""
    return {
        "agents": len(get_agents()),
        "contexts": len(get_contexts()),
        "prompts": len(get_prompts())
    }
