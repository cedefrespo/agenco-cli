# Agenco CLI

Command-line tool to manage agents, contexts, and prompts.

## Installation

```bash
# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/agenco-cli:$PATH"

# Install dependencies for UI
pip install -r ~/agenco-cli/requirements.txt
```

## Usage

### Authentication

Login to Agenco to publish resources without passing `--token` every time:

```bash
# Login (saves token to ~/.agenco/config.json)
agenco login

# Check current user
agenco whoami

# Logout
agenco logout
```

After login, you can publish directly:
```bash
agenco publish prompt fix-bug
agenco publish agent marco
agenco publish context ux-patterns
```

### Interactive Mode
```bash
agenco
```

### Command Line

#### Agents
```bash
agenco agents                    # List all agents
agenco agents show <name>        # Show agent details
agenco agents copy <name>        # Copy agent files content to clipboard
agenco agents add <name> <files> # Add new agent
agenco agents remove <name>      # Remove agent
```

#### Contexts
```bash
agenco contexts                    # List all contexts
agenco contexts show <name>        # Show context details
agenco contexts copy <name>        # Copy context files content to clipboard
agenco contexts add <name> <files> # Add new context
agenco contexts remove <name>      # Remove context
```

#### Prompts
```bash
agenco prompts                     # List all prompts
agenco prompts show <name>         # Show prompt content
agenco prompts copy <name>         # Copy prompt to clipboard
agenco prompts add <name> <text>   # Add new prompt
agenco prompts remove <name>       # Remove prompt
```

#### Search & Stats
```bash
agenco search <query>   # Search across all
agenco stats            # Show statistics
```

#### Publish to Marketplace

After logging in with `agenco login`, publish is simple:

##### From Registry (agents.json, contexts.json, prompts.json)
```bash
agenco publish agent marco           # Publish agent from agents.json
agenco publish context my-docs       # Publish context from contexts.json
agenco publish prompt code-review    # Publish prompt from prompts.json
```

##### From Current Directory (Agents)
```bash
# Interactive: select a .md or .json file in current directory
agenco publish agent

# From specific file
agenco publish agent --file ./system_prompt.md
agenco publish agent --file ./config.json --name my-custom-agent
```

##### From Directory (Contexts)
```bash
# Publish all files in current directory as a context
agenco publish context

# Publish specific directory
agenco publish context --dir ./docs
agenco publish context --dir ./my-project --name project-documentation
```

When publishing from a directory:
- **Text files** (`.md`, `.txt`, `.json`, `.yaml`, `.py`, `.go`, etc.) → bundled as context content
- **Asset files** (`.pdf`, `.doc`, `.png`, `.jpg`, etc.) → uploaded to R2 storage

##### Options
```bash
--file FILE      # Publish agent from specific file (.md or .json)
--dir DIR        # Publish context from directory
--name NAME      # Override resource name
--desc DESC      # Set description
--token TOKEN    # Authentication token
--api-url URL    # API URL (default: https://agt.fly.dev)
--no-assets      # Skip uploading asset files to storage
```

##### Examples
```bash
# Navigate to your project and publish as context
cd ~/projects/my-api-docs
agenco publish context --name api-documentation

# Publish an agent from a markdown file
agenco publish agent --file ./agents/senior-dev.md

# Publish with custom description
agenco publish context --dir ./docs --name my-docs --desc "Project documentation"
```

> **Note:** Publishing requires authentication. Use `agenco login` (recommended) or provide `--token` flag.

## Data Files

- `agents.json` - Agent definitions with file references
- `contexts.json` - Context definitions with file references  
- `prompts.json` - Prompt templates (content stored directly)

## Structure

```
~/agenco-cli/
├── agenco          # Main executable
├── core.py         # Core logic (no dependencies)
├── ui.py           # Interactive UI (rich library)
├── agents.json     # Agents registry
├── contexts.json   # Contexts registry
├── prompts.json    # Prompts registry
└── requirements.txt
```
