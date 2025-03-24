# ui/__init__.py
"""
UI package for Castle Defense game.
Contains user interface components and menus.
Provides backward compatibility for previous menus.py imports.
"""
from .elements import Button, Slider
from .base_menu import Menu
from .building_menu import BuildingMenu
from .tower_menu import TowerMenu
from .castle_menu import CastleMenu

# Export all classes for backward compatibility
__all__ = [
    'Button',
    'Slider',
    'Menu',
    'BuildingMenu',
    'TowerMenu',
    'CastleMenu'
]
