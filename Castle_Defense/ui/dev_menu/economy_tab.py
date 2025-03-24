# ui/dev_menu/economy_tab.py
"""
Economy tab for developer menu
"""
import pygame
from .components import Tab, Slider, Button, DropdownMenu
from config import (
    LOOT_BOSS_BASE_COIN_DROP,
    LOOT_MONSTER_BASE_COIN_DROP,
    LOOT_WAVE_SCALING,
    ITEM_COSTS
)

class EconomyTab(Tab):
    """Tab for adjusting resource generation and costs"""
    def __init__(self, rect, game_instance):
        """
        Initialize economy tab
        
        Args:
            rect: Pygame Rect defining the tab area
            game_instance: Reference to the Game instance
        """
        super().__init__(rect)
        self.game = game_instance
        
        # Store original values for reset
        self.original_item_costs = {
            item: costs.copy() for item, costs in ITEM_COSTS.items()
        }
        self.original_loot_boss_coin_drop = LOOT_BOSS_BASE_COIN_DROP
        self.original_loot_monster_coin_drop = LOOT_MONSTER_BASE_COIN_DROP
        self.original_loot_wave_scaling = LOOT_WAVE_SCALING
        
        # Local copies of values that we'll modify
        self.item_costs = {
            item: costs.copy() for item, costs in ITEM_COSTS.items()
        }
        self.loot_boss_coin_drop = LOOT_BOSS_BASE_COIN_DROP
        self.loot_monster_coin_drop = LOOT_MONSTER_BASE_COIN_DROP
        self.loot_wave_scaling = LOOT_WAVE_SCALING
        
        # Initialize controls
        self._init_controls()
    
    def _init_controls(self):
        """Initialize all controls for this tab"""
        y_pos = self.rect.top + 20
        width = self.rect.width - 40
        
        # Title
        title_text = "Economy Balance"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_pos = (self.rect.left + 20, y_pos)
        y_pos += 30
        
        # Section: Loot Drops
        section_text = "Loot Drops"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Monster coin drop
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Base Monster Coin Drop:",
            self.loot_monster_coin_drop,
            0.5,
            3.0,
            0.5,
            self._set_monster_coin_drop,
            lambda x: f"{x:.1f}"
        ))
        y_pos += 30
        
        # Boss coin drop
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Base Boss Coin Drop:",
            self.loot_boss_coin_drop,
            5,
            20,
            1,
            self._set_boss_coin_drop,
            lambda x: f"{int(x)}"
        ))
        y_pos += 30
        
        # Loot wave scaling
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Loot Wave Scaling:",
            self.loot_wave_scaling,
            0.01,
            0.2,
            0.01,
            self._set_loot_wave_scaling,
            lambda x: f"{x:.2f}"
        ))
        y_pos += 40
        
        # Section: Item Costs
        section_text = "Item Costs"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Item dropdown
        item_names = list(self.item_costs.keys())
        self.item_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Item:",
            item_names,
            0,
            self._item_selected
        )
        self.controls.append(self.item_dropdown)
        y_pos += 30
        
        # Stone cost slider
        self.stone_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Stone Cost:",
            self.item_costs["Unstoppable Force"].get("Stone", 0),
            0,
            10,
            1,
            self._set_stone_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.stone_cost_slider)
        y_pos += 30
        
        # Core cost slider
        self.core_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Core Cost:",
            self.item_costs["Unstoppable Force"].get("Force Core", 0),
            0,
            5,
            1,
            self._set_core_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.core_cost_slider)
        y_pos += 40
        
        # Reset button
        reset_button = Button(
            (self.rect.centerx - 60, self.rect.bottom - 40),
            (120, 30),
            "Reset to Defaults",
            self.reset
        )
        self.controls.append(reset_button)
    
    def _set_monster_coin_drop(self, value):
        """Callback for monster coin drop slider"""
        self.loot_monster_coin_drop = value
        # Update global monster coin drop
        from config_extension import set_loot_monster_base_coin_drop
        set_loot_monster_base_coin_drop(value)
    
    def _set_boss_coin_drop(self, value):
        """Callback for boss coin drop slider"""
        self.loot_boss_coin_drop = int(value)
        # Update global boss coin drop
        from config_extension import set_loot_boss_base_coin_drop
        set_loot_boss_base_coin_drop(int(value))
    
    def _set_loot_wave_scaling(self, value):
        """Callback for loot wave scaling slider"""
        self.loot_wave_scaling = value
        # Update global loot wave scaling
        from config_extension import set_loot_wave_scaling
        set_loot_wave_scaling(value)
    
    def _item_selected(self, index):
        """Callback for item dropdown"""
        item_name = list(self.item_costs.keys())[index]
        # Update sliders with values for selected item
        if item_name == "Unstoppable Force":
            self.stone_cost_slider.value = self.item_costs[item_name].get("Stone", 0)
            self.stone_cost_slider.update_handle()
            
            self.core_cost_slider.value = self.item_costs[item_name].get("Force Core", 0)
            self.core_cost_slider.update_handle()
        else:  # Serene Spirit
            self.stone_cost_slider.value = self.item_costs[item_name].get("Stone", 0)
            self.stone_cost_slider.update_handle()
            
            self.core_cost_slider.value = self.item_costs[item_name].get("Spirit Core", 0)
            self.core_cost_slider.update_handle()
    
    def _set_stone_cost(self, value):
        """Callback for stone cost slider"""
        item_name = list(self.item_costs.keys())[self.item_dropdown.selected_index]
        # Update item stone cost
        self.item_costs[item_name]["Stone"] = int(value)
        # Update global item costs
        from config_extension import update_item_cost
        update_item_cost(item_name, "Stone", int(value))
    
    def _set_core_cost(self, value):
        """Callback for core cost slider"""
        item_name = list(self.item_costs.keys())[self.item_dropdown.selected_index]
        # Determine which core type based on item
        core_type = "Force Core" if item_name == "Unstoppable Force" else "Spirit Core"
        # Update item core cost
        self.item_costs[item_name][core_type] = int(value)
        # Update global item costs
        from config_extension import update_item_cost
        update_item_cost(item_name, core_type, int(value))
    
    def reset(self):
        """Reset all economy values to original values"""
        # Reset loot drops
        from config_extension import (
            set_loot_monster_base_coin_drop,
            set_loot_boss_base_coin_drop,
            set_loot_wave_scaling
        )
        set_loot_monster_base_coin_drop(self.original_loot_monster_coin_drop)
        set_loot_boss_base_coin_drop(self.original_loot_boss_coin_drop)
        set_loot_wave_scaling(self.original_loot_wave_scaling)
        
        # Reset item costs
        for item, costs in self.original_item_costs.items():
            for resource, amount in costs.items():
                from config_extension import update_item_cost
                update_item_cost(item, resource, amount)
        
        # Reset local values
        self.item_costs = {
            item: costs.copy() for item, costs in self.original_item_costs.items()
        }
        self.loot_monster_coin_drop = self.original_loot_monster_coin_drop
        self.loot_boss_coin_drop = self.original_loot_boss_coin_drop
        self.loot_wave_scaling = self.original_loot_wave_scaling
        
        # Update sliders with default values
        for control in self.controls:
            if hasattr(control, 'reset'):
                control.reset()
                
        # Update currently selected item sliders
        self._item_selected(self.item_dropdown.selected_index)
    
    def draw(self, screen):
        """Draw the tab and its controls"""
        super().draw(screen)
        
        # Draw title
        title_text = "Economy Balance"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_rect = title_surface.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title_surface, title_rect)
        
        # Draw section headers
        y_pos = self.rect.top + 60
        
        section_text = "Loot Drops"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, y_pos))
        
        y_pos = self.rect.top + 180
        
        section_text = "Item Costs"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, y_pos))
