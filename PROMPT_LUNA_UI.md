# 🎨 PROMPT PARA LUNA - UI Interactiva para Agenco CLI

## Contexto
Marco creó la lógica core de una CLI llamada `agenco` para administrar agentes, contextos y prompts. Ahora necesito que crees una UI interactiva bonita usando la librería `rich`.

## Ubicación
`~/agenco-cli/ui.py`

## Dependencia
```bash
pip install rich
```

## Lo que necesito

### 1. Archivo `ui.py` con función `run_interactive()`

Esta función se llama desde `agenco` (el ejecutable principal) cuando el usuario ejecuta `agenco` sin argumentos.

### 2. Usar la librería `rich` para:
- Colores y estilos
- Tablas bonitas
- Panels
- Prompts interactivos
- Progress bars (si aplica)
- Syntax highlighting para código/prompts

### 3. Menú principal interactivo

```
╭──────────────────────────────────────╮
│        🚀 AGENCO CLI v1.0            │
│   Manage Agents, Contexts & Prompts  │
╰──────────────────────────────────────╯

📊 Stats: 2 agents | 2 contexts | 5 prompts

[1] 📦 Agents
[2] 📚 Contexts  
[3] 💬 Prompts
[4] 🔍 Search
[5] ❌ Exit

Select option: _
```

### 4. Submenú para cada sección

Por ejemplo, para Agents:

```
╭──────────────────────────────────────╮
│           📦 AGENTS                  │
╰──────────────────────────────────────╯

┌──────────┬────────────────────────────────────┐
│ Name     │ Description                        │
├──────────┼────────────────────────────────────┤
│ marco    │ Backend developer for Go/Python    │
│ luna     │ Frontend developer for React/Next  │
└──────────┴────────────────────────────────────┘

[1] Show agent details
[2] Copy agent to clipboard
[3] Add new agent
[4] Remove agent
[0] Back

Select option: _
```

### 5. Funcionalidades a implementar

- Listar items en tablas con colores
- Mostrar detalles con syntax highlighting
- Copiar al clipboard con feedback visual
- Agregar/eliminar items con confirmación
- Búsqueda interactiva
- Mensajes de éxito/error con colores

### 6. Importar la lógica desde core.py

```python
from core import (
    get_agents, get_agent, get_agent_content, add_agent, remove_agent,
    get_contexts, get_context, get_context_content, add_context, remove_context,
    get_prompts, get_prompt, get_prompt_content, add_prompt, remove_prompt,
    copy_to_clipboard, search_all, get_stats
)
```

### 7. Estilo sugerido

- Usar colores consistentes:
  - 📦 Agents: cyan
  - 📚 Contexts: green
  - 💬 Prompts: yellow
  - ✅ Success: green
  - ❌ Error: red
  - 🔍 Search: magenta

- Bordes redondeados para panels
- Tablas con bordes
- Feedback inmediato al usuario

### 8. Ejemplo de flujo

1. Usuario ejecuta `agenco`
2. Ve menú principal con stats
3. Selecciona "Prompts"
4. Ve lista de prompts en tabla
5. Selecciona "Copy to clipboard"
6. Elige prompt "fix-bug"
7. Ve mensaje "✅ Prompt copied!"
8. Vuelve al menú

## Archivos existentes

- `core.py` - Lógica (ya implementado por Marco)
- `agenco` - Ejecutable principal (ya implementado)
- `agents.json`, `contexts.json`, `prompts.json` - Data

## Ejemplo mínimo de rich

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

console = Console()

# Panel
console.print(Panel("Hello World", title="Demo"))

# Table
table = Table(title="Items")
table.add_column("Name", style="cyan")
table.add_column("Description")
table.add_row("item1", "Description 1")
console.print(table)

# Prompt
name = Prompt.ask("Enter name")

# Syntax highlighting
syntax = Syntax(code, "python", theme="monokai")
console.print(syntax)
```

## Testing

```bash
cd ~/agenco-cli
pip install rich
python -c "from ui import run_interactive; run_interactive()"
# O simplemente:
./agenco
```
