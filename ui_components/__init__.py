"""
UI Components Package
Modular UI components for Agenco CLI
"""

from .common import console, COLORS, VERSION, clear_screen, wait_for_key
from .display import (
    print_header,
    print_stats,
    print_success,
    print_error,
    print_info
)
from .agents import agents_menu
from .contexts import contexts_menu
from .prompts import prompts_menu
from .search import search_menu
from .publish import publish_menu

__all__ = [
    'console',
    'COLORS',
    'VERSION',
    'clear_screen',
    'wait_for_key',
    'print_header',
    'print_stats',
    'print_success',
    'print_error',
    'print_info',
    'agents_menu',
    'contexts_menu',
    'prompts_menu',
    'search_menu',
    'publish_menu',
]
