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

# User config directory
CONFIG_DIR = Path.home() / ".agenco"
CONFIG_FILE = CONFIG_DIR / "config.json"


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
    """Search across agents, contexts, and prompts.
    
    Searches in:
    - Names and descriptions
    - Content of files (for agents and contexts)
    - Prompt text (for prompts)
    """
    query = query.lower()
    results = {
        "agents": [],
        "contexts": [],
        "prompts": []
    }
    
    # Search agents (name, description, AND file contents)
    for agent in get_agents():
        # Check name and description first
        if query in agent.get("name", "").lower() or query in agent.get("description", "").lower():
            results["agents"].append(agent)
            continue
        
        # Also search in file contents
        try:
            content = get_agent_content(agent.get("name", ""))
            if content and query in content.lower():
                results["agents"].append(agent)
        except Exception:
            pass  # Skip if file not readable
    
    # Search contexts (name, description, AND file contents)
    for ctx in get_contexts():
        # Check name and description first
        if query in ctx.get("name", "").lower() or query in ctx.get("description", "").lower():
            results["contexts"].append(ctx)
            continue
        
        # Also search in file contents
        try:
            content = get_context_content(ctx.get("name", ""))
            if content and query in content.lower():
                results["contexts"].append(ctx)
        except Exception:
            pass  # Skip if file not readable
    
    # Search prompts (name, description, AND prompt text)
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


# ============================================
# PUBLISH TO AGENCO MARKETPLACE
# ============================================

def publish_agent(name: str, api_url: str = "https://agt.fly.dev", token: str = None) -> dict:
    """Publish an agent to Agenco marketplace."""
    import requests
    
    # Use saved token if not provided
    if not token:
        token = get_saved_token()
        if not token:
            raise ValueError("Not logged in. Run 'agenco login' first or provide --token")
    
    agent = get_agent(name)
    if not agent:
        raise ValueError(f"Agent '{name}' not found")
    
    # Get agent content from files
    content = get_agent_content(name)
    if not content:
        raise ValueError(f"Agent '{name}' has no content to publish")
    
    # Prepare payload
    payload = {
        "name": agent.get("name"),
        "description": agent.get("description", ""),
        "content": content,
        "tags": agent.get("tags", []),
        "category": agent.get("category", "other"),
        "status": "active",
        "is_public": True,
        "is_free": True,
    }
    
    # Make API request
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.post(
        f"{api_url}/api/v1/publish/agent",
        json=payload,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Failed to publish agent: {response.status_code} - {response.text}")


def publish_context(name: str, api_url: str = "https://agt.fly.dev", token: str = None) -> dict:
    """Publish a context to Agenco marketplace."""
    import requests
    
    # Use saved token if not provided
    if not token:
        token = get_saved_token()
        if not token:
            raise ValueError("Not logged in. Run 'agenco login' first or provide --token")
    
    context = get_context(name)
    if not context:
        raise ValueError(f"Context '{name}' not found")
    
    # Get context content from files
    content = get_context_content(name)
    if not content:
        raise ValueError(f"Context '{name}' has no content to publish")
    
    # Prepare payload
    payload = {
        "name": context.get("name"),
        "description": context.get("description", ""),
        "content": content,
        "tags": context.get("tags", []),
        "category": context.get("category", "other"),
        "content_type": context.get("content_type", "documents"),
        "status": "active",
        "is_public": True,
        "is_free": True,
    }
    
    # Make API request
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.post(
        f"{api_url}/api/v1/publish/context",
        json=payload,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Failed to publish context: {response.status_code} - {response.text}")


def publish_prompt(name: str, api_url: str = "https://agt.fly.dev", token: str = None) -> dict:
    """Publish a prompt to Agenco marketplace."""
    import requests
    
    # Use saved token if not provided
    if not token:
        token = get_saved_token()
        if not token:
            raise ValueError("Not logged in. Run 'agenco login' first or provide --token")
    
    prompt = get_prompt(name)
    if not prompt:
        raise ValueError(f"Prompt '{name}' not found")
    
    prompt_text = prompt.get("prompt", "")
    if not prompt_text:
        raise ValueError(f"Prompt '{name}' has no content to publish")
    
    # Prepare payload
    payload = {
        "name": prompt.get("name"),
        "description": prompt.get("description", ""),
        "content": prompt_text,
        "system_role": prompt.get("system_role", ""),
        "tags": prompt.get("tags", []),
        "category": prompt.get("category", "coding"),
        "status": "active",
        "is_public": True,
        "is_free": True,
    }
    
    # Make API request
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    response = requests.post(
        f"{api_url}/api/v1/prompts/publish",
        json=payload,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Failed to publish prompt: {response.status_code} - {response.text}")


# ============================================
# AUTHENTICATION
# ============================================

def get_config() -> dict:
    """Load user config from ~/.agenco/config.json"""
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config: dict) -> None:
    """Save user config to ~/.agenco/config.json"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_saved_token() -> Optional[str]:
    """Get saved auth token from config."""
    config = get_config()
    return config.get("token")


def login(email: str, password: str, api_url: str = "https://agt.fly.dev") -> dict:
    """Login to Agenco and save token."""
    import requests
    
    # Step 1: Initial login
    response = requests.post(
        f"{api_url}/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check if 2FA is required
    if data.get("requires_2fa"):
        session_id = data.get("session_id")
        print(f"\n2FA code sent to {email}")
        code = input("Enter 2FA code: ").strip()
        
        # Step 2: Verify 2FA
        response = requests.post(
            f"{api_url}/api/v1/auth/verify-2fa",
            json={"session_id": session_id, "code": code}
        )
        
        if response.status_code != 200:
            raise Exception(f"2FA verification failed: {response.status_code} - {response.text}")
        
        data = response.json()
    
    # Extract token from response
    token = data.get("token") or data.get("access_token")
    user = data.get("user", {})
    
    if not token:
        raise Exception("No token received from server")
    
    # Save token and user info
    config = {
        "token": token,
        "user": {
            "email": user.get("email"),
            "name": user.get("name"),
            "id": user.get("id")
        },
        "api_url": api_url
    }
    save_config(config)
    return data


def logout() -> None:
    """Remove saved authentication."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()


def get_current_user() -> Optional[dict]:
    """Get current logged-in user info."""
    config = get_config()
    return config.get("user")


def is_logged_in() -> bool:
    """Check if user is logged in."""
    return get_saved_token() is not None


# ============================================
# DIRECTORY-BASED PUBLISH
# ============================================

# File extensions that are context-worthy (text-based)
TEXT_EXTENSIONS = {'.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml', '.html', '.css', '.js', '.ts', '.py', '.go', '.rs', '.java', '.c', '.cpp', '.h', '.hpp', '.sh', '.bash', '.zsh', '.sql', '.r', '.rb', '.php', '.swift', '.kt', '.scala', '.lua', '.vim', '.el'}

# File extensions that should be uploaded as assets to R2
ASSET_EXTENSIONS = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.mp3', '.mp4', '.wav', '.zip', '.tar', '.gz'}


def get_directory_files(directory: Path = None) -> dict:
    """
    Scan a directory and categorize files.
    
    Returns:
        dict with 'text_files' (for context) and 'asset_files' (for R2 upload)
    """
    if directory is None:
        directory = Path.cwd()
    
    directory = Path(directory)
    
    text_files = []
    asset_files = []
    other_files = []
    
    # Scan directory (non-recursive for now, can add option later)
    for item in directory.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            ext = item.suffix.lower()
            file_info = {
                'name': item.name,
                'path': str(item.absolute()),
                'extension': ext,
                'size': item.stat().st_size
            }
            
            if ext in TEXT_EXTENSIONS:
                text_files.append(file_info)
            elif ext in ASSET_EXTENSIONS:
                asset_files.append(file_info)
            else:
                other_files.append(file_info)
    
    return {
        'text_files': text_files,
        'asset_files': asset_files,
        'other_files': other_files,
        'directory': str(directory),
        'directory_name': directory.name
    }


def read_text_file(filepath: str) -> str:
    """Read a text file and return its content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def upload_asset_to_r2(filepath: str, api_url: str = "https://agt.fly.dev", token: str = None) -> dict:
    """Upload an asset file to R2 storage via API."""
    import requests
    
    if not token:
        token = get_saved_token()
        if not token:
            raise ValueError("Not logged in. Run 'agenco login' first")
    
    file_path = Path(filepath)
    
    # Prepare multipart upload
    with open(file_path, 'rb') as f:
        files = {
            'file': (file_path.name, f, 'application/octet-stream')
        }
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{api_url}/api/v1/upload/asset",
            files=files,
            headers=headers
        )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Failed to upload asset: {response.status_code} - {response.text}")


def publish_agent_from_file(
    filepath: str, 
    name: str = None,
    description: str = None,
    api_url: str = "https://agt.fly.dev", 
    token: str = None
) -> dict:
    """
    Publish an agent from a single .md or .json file.
    
    Args:
        filepath: Path to the .md or .json file
        name: Agent name (defaults to filename without extension)
        description: Agent description
        api_url: API URL
        token: Auth token
    """
    import requests
    
    if not token:
        token = get_saved_token()
        if not token:
            raise ValueError("Not logged in. Run 'agenco login' first or provide --token")
    
    file_path = Path(filepath)
    if not file_path.exists():
        raise ValueError(f"File not found: {filepath}")
    
    ext = file_path.suffix.lower()
    if ext not in {'.md', '.json'}:
        raise ValueError(f"Invalid file type: {ext}. Only .md and .json are supported for agents.")
    
    # Determine name
    if not name:
        name = file_path.stem  # filename without extension
    
    # Read content
    if ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            content = json.dumps(data, indent=2)
            if not description:
                description = data.get('description', f'Agent from {file_path.name}')
    else:
        content = read_text_file(str(file_path))
        if not description:
            # Try to extract description from first line or use default
            first_line = content.split('\n')[0].strip()
            if first_line.startswith('#'):
                description = first_line.lstrip('#').strip()
            else:
                description = f'Agent from {file_path.name}'
    
    # Prepare payload
    payload = {
        "name": name,
        "description": description,
        "content": content,
        "tags": [],
        "category": "other",
        "status": "active",
        "is_public": True,
        "is_free": True,
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(
        f"{api_url}/api/v1/publish/agent",
        json=payload,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Failed to publish agent: {response.status_code} - {response.text}")


def publish_context_from_directory(
    directory: str = None,
    name: str = None,
    description: str = None,
    api_url: str = "https://agt.fly.dev",
    token: str = None,
    include_assets: bool = True
) -> dict:
    """
    Publish a context from all files in a directory.
    
    - .md and other text files are bundled as context content
    - .pdf and other assets are uploaded to R2
    
    Args:
        directory: Directory path (defaults to current directory)
        name: Context name (defaults to directory name)
        description: Context description
        api_url: API URL
        token: Auth token
        include_assets: Whether to upload asset files to R2
    """
    import requests
    
    if not token:
        token = get_saved_token()
        if not token:
            raise ValueError("Not logged in. Run 'agenco login' first or provide --token")
    
    # Get directory info
    dir_path = Path(directory) if directory else Path.cwd()
    files_info = get_directory_files(dir_path)
    
    if not name:
        name = files_info['directory_name']
    
    if not description:
        description = f"Context from {files_info['directory_name']} directory"
    
    # Bundle text content
    content_parts = []
    for file_info in files_info['text_files']:
        try:
            file_content = read_text_file(file_info['path'])
            content_parts.append(f"# File: {file_info['name']}\n\n{file_content}")
        except Exception as e:
            print(f"[WARN] Could not read {file_info['name']}: {e}")
    
    if not content_parts:
        raise ValueError("No text files found in directory to publish")
    
    content = "\n\n---\n\n".join(content_parts)
    
    # Upload assets if requested
    asset_urls = []
    if include_assets and files_info['asset_files']:
        print(f"\n[Info] Uploading {len(files_info['asset_files'])} asset files to storage...")
        for asset_info in files_info['asset_files']:
            try:
                result = upload_asset_to_r2(asset_info['path'], api_url, token)
                asset_urls.append({
                    'name': asset_info['name'],
                    'url': result.get('url', ''),
                    'type': asset_info['extension']
                })
                print(f"  [OK] Uploaded {asset_info['name']}")
            except Exception as e:
                print(f"  [WARN] Failed to upload {asset_info['name']}: {e}")
    
    # Prepare payload
    payload = {
        "name": name,
        "description": description,
        "content": content,
        "tags": [],
        "category": "other",
        "content_type": "documents",
        "status": "active",
        "is_public": True,
        "is_free": True,
    }
    
    # Add asset URLs if any were uploaded
    if asset_urls:
        payload["assets"] = asset_urls
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(
        f"{api_url}/api/v1/publish/context",
        json=payload,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise Exception(f"Failed to publish context: {response.status_code} - {response.text}")

