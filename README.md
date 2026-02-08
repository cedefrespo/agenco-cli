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
```bash
# Publish agents, contexts, or prompts to Agenco marketplace
agenco publish agent <name>          # Publish an agent
agenco publish context <name>        # Publish a context
agenco publish prompt <name>         # Publish a prompt

# With authentication token
agenco publish agent marco --token abc123

# Custom API URL (for testing)
agenco publish context ux-patterns --api-url http://localhost:8080

# Using environment variable for token
export AGENCO_TOKEN='your-token-here'
agenco publish prompt code-review
```

> **Note:** Publishing requires authentication. Set `AGENCO_TOKEN` environment variable or use `--token` flag.

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
