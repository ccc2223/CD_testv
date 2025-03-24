# ui/menus.py
"""
Legacy import file for backward compatibility
All implementations have been moved to separate modules
"""

# Re-export everything from the UI modules
from .elements import Button, Slider
from .base_menu import Menu
from .building_menu import BuildingMenu
from .tower_menu import TowerMenu

# Keep everything in the old namespace for backward compatibility
__all__ = [
    'Button',
    'Slider',
    'Menu',
    'BuildingMenu',
    'TowerMenu'
]
