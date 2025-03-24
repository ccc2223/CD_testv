# ui/dev_menu/building_tab.py
"""
Building configuration tab for developer menu
"""
import pygame
from .components import Tab, Slider, Button, DropdownMenu
from config import (
    CASTLE_HEALTH_UPGRADE_COST,
    CASTLE_DAMAGE_REDUCTION_UPGRADE_COST,
    CASTLE_HEALTH_REGEN_UPGRADE_COST,
    CASTLE_HEALTH_UPGRADE_MULTIPLIER,
    CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER,
    CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER,
    MINE_INITIAL_PRODUCTION,
    MINE_PRODUCTION_MULTIPLIER,
    MINE_UPGRADE_COST,
    MINE_UPGRADE_TIME_MULTIPLIER,
    MINE_INITIAL_UPGRADE_TIME,
    CORESMITH_CRAFTING_TIME
)

class BuildingTab(Tab):
    """Tab for adjusting building upgrade costs and settings"""
    def __init__(self, rect, game_instance):
        """
        Initialize building tab
        
        Args:
            rect: Pygame Rect defining the tab area
            game_instance: Reference to the Game instance
        """
        super().__init__(rect)
        self.game = game_instance
        
        # Store original values for reset
        self.original_castle_health_cost = CASTLE_HEALTH_UPGRADE_COST.copy()
        self.original_castle_dr_cost = CASTLE_DAMAGE_REDUCTION_UPGRADE_COST.copy()
        self.original_castle_regen_cost = CASTLE_HEALTH_REGEN_UPGRADE_COST.copy()
        self.original_castle_health_mult = CASTLE_HEALTH_UPGRADE_MULTIPLIER
        self.original_castle_dr_mult = CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER
        self.original_castle_regen_mult = CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
        self.original_mine_initial_production = MINE_INITIAL_PRODUCTION
        self.original_mine_production_multiplier = MINE_PRODUCTION_MULTIPLIER
        self.original_mine_upgrade_cost = MINE_UPGRADE_COST.copy()
        self.original_mine_upgrade_time_multiplier = MINE_UPGRADE_TIME_MULTIPLIER
        self.original_mine_initial_upgrade_time = MINE_INITIAL_UPGRADE_TIME
        self.original_coresmith_crafting_time = CORESMITH_CRAFTING_TIME
        
        # Local copies of values that we'll modify
        self.castle_health_cost = CASTLE_HEALTH_UPGRADE_COST.copy()
        self.castle_dr_cost = CASTLE_DAMAGE_REDUCTION_UPGRADE_COST.copy()
        self.castle_regen_cost = CASTLE_HEALTH_REGEN_UPGRADE_COST.copy()
        self.castle_health_mult = CASTLE_HEALTH_UPGRADE_MULTIPLIER
        self.castle_dr_mult = CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER
        self.castle_regen_mult = CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
        self.mine_initial_production = MINE_INITIAL_PRODUCTION
        self.mine_production_multiplier = MINE_PRODUCTION_MULTIPLIER
        self.mine_upgrade_cost = MINE_UPGRADE_COST.copy()
        self.mine_upgrade_time_multiplier = MINE_UPGRADE_TIME_MULTIPLIER
        self.mine_initial_upgrade_time = MINE_INITIAL_UPGRADE_TIME
        self.coresmith_crafting_time = CORESMITH_CRAFTING_TIME
        
        # Which building to configure
        self.building_types = ["Castle", "Mine", "Coresmith"]
        self.current_building = "Castle"
        
        # Which upgrade path for castle
        self.castle_upgrade_types = ["Health", "Damage Reduction", "Health Regen"]
        self.current_castle_upgrade = "Health"
        
        # Initialize controls
        self._init_controls()
    
    def _init_controls(self):
        """Initialize all controls for this tab"""
        y_pos = self.rect.top + 20
        width = self.rect.width - 40
        
        # Title
        title_text = "Building Configuration"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_pos = (self.rect.left + 20, y_pos)
        y_pos += 30
        
        # Building selection dropdown
        self.building_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Building Type:",
            self.building_types,
            0,
            self._building_selected
        )
        self.controls.append(self.building_dropdown)
        y_pos += 40
        
        # Section: Castle Configuration
        self.castle_section_y = y_pos
        self.castle_section_text = "Castle Configuration"
        y_pos += 25
        
        # Castle upgrade type dropdown
        self.castle_upgrade_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Upgrade Type:",
            self.castle_upgrade_types,
            0,
            self._castle_upgrade_selected
        )
        self.controls.append(self.castle_upgrade_dropdown)
        y_pos += 30
        
        # Castle upgrade cost sliders
        # Stone cost
        self.castle_stone_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Stone Cost:",
            self.castle_health_cost.get("Stone", 0),
            0,
            200,
            5,
            self._set_castle_stone_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_stone_cost_slider)
        y_pos += 30
        
        # Iron cost
        self.castle_iron_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Iron Cost:",
            self.castle_health_cost.get("Iron", 0),
            0,
            100,
            5,
            self._set_castle_iron_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_iron_cost_slider)
        y_pos += 30
        
        # Copper cost
        self.castle_copper_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Copper Cost:",
            self.castle_health_cost.get("Copper", 0),
            0,
            50,
            1,
            self._set_castle_copper_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_copper_cost_slider)
        y_pos += 30
        
        # Monster Coins cost
        self.castle_monster_coins_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Monster Coins Cost:",
            self.castle_health_cost.get("Monster Coins", 1),
            0,
            20,
            1,
            self._set_castle_monster_coins_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_monster_coins_cost_slider)
        y_pos += 30
        
        # Castle upgrade multiplier
        self.castle_upgrade_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Upgrade Multiplier:",
            self.castle_health_mult,
            1.1,
            2.0,
            0.1,
            self._set_castle_upgrade_multiplier
        )
        self.controls.append(self.castle_upgrade_multiplier_slider)
        y_pos += 40
        
        # Section: Mine Configuration
        self.mine_section_y = y_pos
        self.mine_section_text = "Mine Configuration"
        y_pos += 25
        
        # Mine initial production
        self.mine_initial_production_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Initial Production Rate:",
            self.mine_initial_production,
            0.5,
            3.0,
            0.1,
            self._set_mine_initial_production
        )
        self.controls.append(self.mine_initial_production_slider)
        y_pos += 30
        
        # Mine production multiplier
        self.mine_production_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Production Multiplier:",
            self.mine_production_multiplier,
            1.0,
            1.5,
            0.05,
            self._set_mine_production_multiplier
        )
        self.controls.append(self.mine_production_multiplier_slider)
        y_pos += 30
        
        # Mine upgrade time multiplier
        self.mine_upgrade_time_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Upgrade Time Multiplier:",
            self.mine_upgrade_time_multiplier,
            1.0,
            3.0,
            0.1,
            self._set_mine_upgrade_time_multiplier
        )
        self.controls.append(self.mine_upgrade_time_multiplier_slider)
        y_pos += 30
        
        # Mine initial upgrade time
        self.mine_initial_upgrade_time_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Initial Upgrade Time:",
            self.mine_initial_upgrade_time,
            1.0,
            30.0,
            1.0,
            self._set_mine_initial_upgrade_time,
            lambda x: f"{int(x)} seconds"
        )
        self.controls.append(self.mine_initial_upgrade_time_slider)
        y_pos += 30
        
        # Mine upgrade boss core cost
        self.mine_boss_core_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Boss Core Upgrade Cost:",
            self.mine_upgrade_cost.get("Boss Cores", 1),
            1,
            5,
            1,
            self._set_mine_boss_core_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.mine_boss_core_cost_slider)
        y_pos += 40
        
        # Section: Coresmith Configuration
        self.coresmith_section_y = y_pos
        self.coresmith_section_text = "Coresmith Configuration"
        y_pos += 25
        
        # Coresmith crafting time
        self.coresmith_crafting_time_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Crafting Time:",
            self.coresmith_crafting_time,
            5.0,
            60.0,
            5.0,
            self._set_coresmith_crafting_time,
            lambda x: f"{int(x)} seconds"
        )
        self.controls.append(self.coresmith_crafting_time_slider)
        y_pos += 40
        
        # Reset button
        reset_button = Button(
            (self.rect.centerx - 60, self.rect.bottom - 40),
            (120, 30),
            "Reset to Defaults",
            self.reset
        )
        self.controls.append(reset_button)
        
        # Set initial visibility
        self._update_section_visibility()
    
    def _update_section_visibility(self):
        """Update visibility of different building section controls"""
        # Castle section controls
        castle_controls = [
            self.castle_upgrade_dropdown,
            self.castle_stone_cost_slider,
            self.castle_iron_cost_slider,
            self.castle_copper_cost_slider,
            self.castle_monster_coins_cost_slider,
            self.castle_upgrade_multiplier_slider
        ]
        
        # Mine section controls
        mine_controls = [
            self.mine_initial_production_slider,
            self.mine_production_multiplier_slider,
            self.mine_upgrade_time_multiplier_slider,
            self.mine_initial_upgrade_time_slider,
            self.mine_boss_core_cost_slider
        ]
        
        # Coresmith section controls
        coresmith_controls = [
            self.coresmith_crafting_time_slider
        ]
        
        # Set visibility based on current building type
        for control in castle_controls:
            control.visible = (self.current_building == "Castle")
        
        for control in mine_controls:
            control.visible = (self.current_building == "Mine")
        
        for control in coresmith_controls:
            control.visible = (self.current_building == "Coresmith")
    
    def _building_selected(self, index):
        """Callback for building type selection"""
        self.current_building = self.building_types[index]
        self._update_section_visibility()
    
    def _castle_upgrade_selected(self, index):
        """Callback for castle upgrade type selection"""
        self.current_castle_upgrade = self.castle_upgrade_types[index]
        
        # Update cost sliders based on selected upgrade type
        if self.current_castle_upgrade == "Health":
            costs = self.castle_health_cost
            multiplier = self.castle_health_mult
        elif self.current_castle_upgrade == "Damage Reduction":
            costs = self.castle_dr_cost
            multiplier = self.castle_dr_mult
        elif self.current_castle_upgrade == "Health Regen":
            costs = self.castle_regen_cost
            multiplier = self.castle_regen_mult
        
        # Update sliders with current costs
        self.castle_stone_cost_slider.value = costs.get("Stone", 0)
        self.castle_stone_cost_slider.update_handle()
        
        self.castle_iron_cost_slider.value = costs.get("Iron", 0)
        self.castle_iron_cost_slider.update_handle()
        
        self.castle_copper_cost_slider.value = costs.get("Copper", 0)
        self.castle_copper_cost_slider.update_handle()
        
        self.castle_monster_coins_cost_slider.value = costs.get("Monster Coins", 0)
        self.castle_monster_coins_cost_slider.update_handle()
        
        self.castle_upgrade_multiplier_slider.value = multiplier
        self.castle_upgrade_multiplier_slider.update_handle()
    
    def _set_castle_stone_cost(self, value):
        """Callback for castle stone cost slider"""
        if self.current_castle_upgrade == "Health":
            self.castle_health_cost["Stone"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Stone", int(value))
        elif self.current_castle_upgrade == "Damage Reduction":
            self.castle_dr_cost["Stone"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Stone", int(value))
        elif self.current_castle_upgrade == "Health Regen":
            self.castle_regen_cost["Stone"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Stone", int(value))
    
    def _set_castle_iron_cost(self, value):
        """Callback for castle iron cost slider"""
        if self.current_castle_upgrade == "Health":
            self.castle_health_cost["Iron"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Iron", int(value))
        elif self.current_castle_upgrade == "Damage Reduction":
            self.castle_dr_cost["Iron"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Iron", int(value))
        elif self.current_castle_upgrade == "Health Regen":
            self.castle_regen_cost["Iron"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Iron", int(value))
    
    def _set_castle_copper_cost(self, value):
        """Callback for castle copper cost slider"""
        if self.current_castle_upgrade == "Health":
            self.castle_health_cost["Copper"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Copper", int(value))
        elif self.current_castle_upgrade == "Damage Reduction":
            self.castle_dr_cost["Copper"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Copper", int(value))
        elif self.current_castle_upgrade == "Health Regen":
            self.castle_regen_cost["Copper"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Copper", int(value))
    
    def _set_castle_monster_coins_cost(self, value):
        """Callback for castle monster coins cost slider"""
        if self.current_castle_upgrade == "Health":
            self.castle_health_cost["Monster Coins"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Monster Coins", int(value))
        elif self.current_castle_upgrade == "Damage Reduction":
            self.castle_dr_cost["Monster Coins"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Monster Coins", int(value))
        elif self.current_castle_upgrade == "Health Regen":
            self.castle_regen_cost["Monster Coins"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Monster Coins", int(value))
    
    def _set_castle_upgrade_multiplier(self, value):
        """Callback for castle upgrade multiplier slider"""
        if self.current_castle_upgrade == "Health":
            self.castle_health_mult = value
            from config_extension import set_castle_health_upgrade_multiplier
            set_castle_health_upgrade_multiplier(value)
        elif self.current_castle_upgrade == "Damage Reduction":
            self.castle_dr_mult = value
            from config_extension import set_castle_damage_reduction_upgrade_multiplier
            set_castle_damage_reduction_upgrade_multiplier(value)
        elif self.current_castle_upgrade == "Health Regen":
            self.castle_regen_mult = value
            from config_extension import set_castle_health_regen_upgrade_multiplier
            set_castle_health_regen_upgrade_multiplier(value)
    
    def _set_mine_initial_production(self, value):
        """Callback for mine initial production slider"""
        self.mine_initial_production = value
        from config_extension import set_mine_initial_production
        set_mine_initial_production(value)
    
    def _set_mine_production_multiplier(self, value):
        """Callback for mine production multiplier slider"""
        self.mine_production_multiplier = value
        from config_extension import set_mine_production_multiplier
        set_mine_production_multiplier(value)
    
    def _set_mine_upgrade_time_multiplier(self, value):
        """Callback for mine upgrade time multiplier slider"""
        self.mine_upgrade_time_multiplier = value
        # Update the config value
        module = __import__('sys').modules['config']
        module.MINE_UPGRADE_TIME_MULTIPLIER = value
    
    def _set_mine_initial_upgrade_time(self, value):
        """Callback for mine initial upgrade time slider"""
        self.mine_initial_upgrade_time = value
        # Update the config value
        module = __import__('sys').modules['config']
        module.MINE_INITIAL_UPGRADE_TIME = value
    
    def _set_mine_boss_core_cost(self, value):
        """Callback for mine boss core cost slider"""
        self.mine_upgrade_cost["Boss Cores"] = int(value)
        # Update the config value
        module = __import__('sys').modules['config']
        module.MINE_UPGRADE_COST = self.mine_upgrade_cost.copy()
    
    def _set_coresmith_crafting_time(self, value):
        """Callback for coresmith crafting time slider"""
        self.coresmith_crafting_time = value
        # Update the config value
        module = __import__('sys').modules['config']
        module.CORESMITH_CRAFTING_TIME = value
    
    def reset(self):
        """Reset all building values to defaults"""
        # Reset Castle values
        from config_extension import (
            reset_castle_upgrade_costs,
            set_castle_health_upgrade_multiplier,
            set_castle_damage_reduction_upgrade_multiplier,
            set_castle_health_regen_upgrade_multiplier
        )
        reset_castle_upgrade_costs()
        set_castle_health_upgrade_multiplier(self.original_castle_health_mult)
        set_castle_damage_reduction_upgrade_multiplier(self.original_castle_dr_mult)
        set_castle_health_regen_upgrade_multiplier(self.original_castle_regen_mult)
        
        # Reset Mine values
        from config_extension import (
            set_mine_initial_production,
            set_mine_production_multiplier
        )
        set_mine_initial_production(self.original_mine_initial_production)
        set_mine_production_multiplier(self.original_mine_production_multiplier)
        
        # Reset other config values
        module = __import__('sys').modules['config']
        module.MINE_UPGRADE_TIME_MULTIPLIER = self.original_mine_upgrade_time_multiplier
        module.MINE_INITIAL_UPGRADE_TIME = self.original_mine_initial_upgrade_time
        module.MINE_UPGRADE_COST = self.original_mine_upgrade_cost.copy()
        module.CORESMITH_CRAFTING_TIME = self.original_coresmith_crafting_time
        
        # Reset local values
        self.castle_health_cost = self.original_castle_health_cost.copy()
        self.castle_dr_cost = self.original_castle_dr_cost.copy()
        self.castle_regen_cost = self.original_castle_regen_cost.copy()
        self.castle_health_mult = self.original_castle_health_mult
        self.castle_dr_mult = self.original_castle_dr_mult
        self.castle_regen_mult = self.original_castle_regen_mult
        self.mine_initial_production = self.original_mine_initial_production
        self.mine_production_multiplier = self.original_mine_production_multiplier
        self.mine_upgrade_cost = self.original_mine_upgrade_cost.copy()
        self.mine_upgrade_time_multiplier = self.original_mine_upgrade_time_multiplier
        self.mine_initial_upgrade_time = self.original_mine_initial_upgrade_time
        self.coresmith_crafting_time = self.original_coresmith_crafting_time
        
        # Update sliders
        for control in self.controls:
            if hasattr(control, 'reset'):
                control.reset()
        
        # Update castle upgrade dropdowns
        self._castle_upgrade_selected(self.castle_upgrade_dropdown.selected_index)
    
    def draw(self, screen):
        """Draw the tab and its controls"""
        super().draw(screen)
        
        # Draw title
        title_text = "Building Configuration"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_rect = title_surface.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title_surface, title_rect)
        
        # Draw section headers based on current building
        if self.current_building == "Castle":
            section_text = "Castle Configuration"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, self.castle_section_y))
        
        elif self.current_building == "Mine":
            section_text = "Mine Configuration"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, self.mine_section_y))
        
        elif self.current_building == "Coresmith":
            section_text = "Coresmith Configuration"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, self.coresmith_section_y))
