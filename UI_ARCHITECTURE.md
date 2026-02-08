# UI Architecture

The UI has been refactored into modular components for better maintainability.

## Structure

```
~/agenco-cli/
├── ui.py                    # Main entry point (70 lines)
├── ui_components/
│   ├── __init__.py         # Package exports
│   ├── common.py           # Shared constants & utilities
│   ├── display.py          # Display functions (headers, messages)
│   ├── agents.py           # Agents menu & functions
│   ├── contexts.py         # Contexts menu & functions
│   ├── prompts.py          # Prompts menu & functions
│   └── search.py           # Search functionality
```

## Benefits

- **Modular**: Each resource type (agents/contexts/prompts) in separate file
- **Maintainable**: Small, focused files (~150 lines each)
- **Reusable**: Common functions in shared modules
- **Testable**: Easy to test individual components
- **Readable**: Clear separation of concerns

## File Sizes

- `ui.py`: ~70 lines (was 733)
- `common.py`: ~30 lines
- `display.py`: ~60 lines
- `agents.py`: ~150 lines
- `contexts.py`: ~150 lines
- `prompts.py`: ~155 lines
- `search.py`: ~110 lines

Total: Same functionality, better organized
