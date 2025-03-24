# ui/dev_menu/buildings_tab.py
"""
Buildings tab for developer menu
"""
import pygame
from .components import Tab, Slider, Button, DropdownMenu
from config import (
    MINE_INITIAL_PRODUCTION,
    MINE_PRODUCTION_MULTIPLIER,
    MINE_UPGRADE_TIME_MULTIPLIER,
    MINE_INITIAL_UPGRADE_TIME,
    MINE_UPGRADE_COST,
    CORESMITH_CRAFTING_TIME,
    CASTLE_HEALTH_UPGRADE_COST,
    CASTLE_DAMAGE_REDUCTION_UPGRADE_COST,
    CASTLE_HEALTH_REGEN_UPGRADE_COST,
    CASTLE_HEALTH_UPGRADE_MULTIPLIER,
    CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER,
    CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
)

class BuildingsTab(Tab):
    """Tab for adjusting buildings and castle settings"""
    def __init__(self, rect, game_instance):
        """
        Initialize buildings tab
        
        Args:
            rect: Pygame Rect defining the tab area
            game_instance: Reference to the Game instance
        """
        super().__init__(rect)
        self.game = game_instance
        
        # Store original values for reset
        self.original_mine_initial_production = MINE_INITIAL_PRODUCTION
        self.original_mine_production_multiplier = MINE_PRODUCTION_MULTIPLIER
        self.original_mine_upgrade_time_multiplier = MINE_UPGRADE_TIME_MULTIPLIER
        self.original_mine_initial_upgrade_time = MINE_INITIAL_UPGRADE_TIME
        self.original_mine_upgrade_cost = MINE_UPGRADE_COST.copy()
        self.original_coresmith_crafting_time = CORESMITH_CRAFTING_TIME
        self.original_castle_health_cost = CASTLE_HEALTH_UPGRADE_COST.copy()
        self.original_castle_dr_cost = CASTLE_DAMAGE_REDUCTION_UPGRADE_COST.copy()
        self.original_castle_regen_cost = CASTLE_HEALTH_REGEN_UPGRADE_COST.copy()
        self.original_castle_health_mult = CASTLE_HEALTH_UPGRADE_MULTIPLIER
        self.original_castle_dr_mult = CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER
        self.original_castle_regen_mult = CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
        
        # Local copies of values that we'll modify
        self.mine_initial_production = MINE_INITIAL_PRODUCTION
        self.mine_production_multiplier = MINE_PRODUCTION_MULTIPLIER
        self.mine_upgrade_time_multiplier = MINE_UPGRADE_TIME_MULTIPLIER
        self.mine_initial_upgrade_time = MINE_INITIAL_UPGRADE_TIME
        self.mine_upgrade_cost = MINE_UPGRADE_COST.copy()
        self.coresmith_crafting_time = CORESMITH_CRAFTING_TIME
        self.castle_health_cost = CASTLE_HEALTH_UPGRADE_COST.copy()
        self.castle_dr_cost = CASTLE_DAMAGE_REDUCTION_UPGRADE_COST.copy()
        self.castle_regen_cost = CASTLE_HEALTH_REGEN_UPGRADE_COST.copy()
        self.castle_health_mult = CASTLE_HEALTH_UPGRADE_MULTIPLIER
        self.castle_dr_mult = CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER
        self.castle_regen_mult = CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
        
        # Selected values for the dropdown
        self.selected_building_type = "Mine"
        self.selected_upgrade_type = "health"
        
        # Initialize controls
        self._init_controls()
    
    def _init_controls(self):
        """Initialize all controls for this tab"""
        y_pos = self.rect.top + 20
        width = self.rect.width - 40
        
        # Title
        title_text = "Buildings Balance"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_pos = (self.rect.left + 20, y_pos)
        y_pos += 30
        
        # Section: Building Type Selection
        section_text = "Building Type"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Building type dropdown
        building_types = ["Mine", "Coresmith", "Castle"]
        self.building_type_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Building Type:",
            building_types,
            0,
            self._building_type_selected
        )
        self.controls.append(self.building_type_dropdown)
        y_pos += 40
        
        # Section: Mine Settings
        self.mine_section_y = y_pos
        section_text = "Mine Settings"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Mine initial production
        self.mine_initial_production_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Initial Production Rate:",
            self.mine_initial_production,
            0.5,
            5.0,
            0.1,
            self._set_mine_initial_production,
            lambda x: f"{x:.1f}"
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
            2.0,
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
            "Initial Upgrade Time (s):",
            self.mine_initial_upgrade_time,
            5,
            30,
            1,
            self._set_mine_initial_upgrade_time,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.mine_initial_upgrade_time_slider)
        y_pos += 30
        
        # Mine upgrade cost (Boss Cores)
        self.mine_upgrade_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Upgrade Cost (Boss Cores):",
            self.mine_upgrade_cost.get("Boss Cores", 1),
            1,
            5,
            1,
            self._set_mine_upgrade_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.mine_upgrade_cost_slider)
        self.mine_section_end_y = y_pos + 40
        
        # Section: Coresmith Settings
        self.coresmith_section_y = y_pos
        y_pos += 40
        section_text = "Coresmith Settings"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Coresmith crafting time
        self.coresmith_crafting_time_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Crafting Time (s):",
            self.coresmith_crafting_time,
            10,
            60,
            5,
            self._set_coresmith_crafting_time,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.coresmith_crafting_time_slider)
        self.coresmith_section_end_y = y_pos + 40
        
        # Section: Castle Settings
        self.castle_section_y = y_pos
        y_pos += 40
        section_text = "Castle Settings"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Castle upgrade type dropdown
        upgrade_types = ["Health", "Damage Reduction", "Health Regen"]
        self.castle_upgrade_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Upgrade Type:",
            upgrade_types,
            0,
            self._castle_upgrade_type_selected
        )
        self.controls.append(self.castle_upgrade_dropdown)
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
        y_pos += 30
        
        # Castle stone cost
        self.castle_stone_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Stone Cost:",
            self.castle_health_cost.get("Stone", 75),
            10,
            200,
            5,
            self._set_castle_stone_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_stone_cost_slider)
        y_pos += 30
        
        # Castle iron cost
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
        
        # Castle copper cost
        self.castle_copper_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Copper Cost:",
            self.castle_health_cost.get("Copper", 0),
            0,
            50,
            5,
            self._set_castle_copper_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_copper_cost_slider)
        y_pos += 30
        
        # Castle Monster Coin cost
        self.castle_monster_coin_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Monster Coin Cost:",
            self.castle_health_cost.get("Monster Coins", 1),
            1,
            20,
            1,
            self._set_castle_monster_coin_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.castle_monster_coin_cost_slider)
        self.castle_section_end_y = y_pos + 40
        
        # Reset button
        reset_button = Button(
            (self.rect.centerx - 60, self.rect.bottom - 40),
            (120, 30),
            "Reset to Defaults",
            self.reset
        )
        self.controls.append(reset_button)
        
        # Hide sections based on selected building type
        self._update_visible_sections()
    
    def _building_type_selected(self, index):
        """Callback for building type dropdown"""
        building_types = ["Mine", "Coresmith", "Castle"]
        self.selected_building_type = building_types[index]
        self._update_visible_sections()
    
    def _castle_upgrade_type_selected(self, index):
        """Callback for castle upgrade type dropdown"""
        upgrade_types = ["health", "damage_reduction", "health_regen"]
        self.selected_upgrade_type = upgrade_types[index]
        
        # Update sliders with values for selected upgrade type
        if self.selected_upgrade_type == "health":
            # Update multiplier slider
            self.castle_upgrade_multiplier_slider.value = self.castle_health_mult
            self.castle_upgrade_multiplier_slider.update_handle()
            
            # Update cost sliders
            self.castle_stone_cost_slider.value = self.castle_health_cost.get("Stone", 75)
            self.castle_stone_cost_slider.update_handle()
            
            self.castle_iron_cost_slider.value = self.castle_health_cost.get("Iron", 0)
            self.castle_iron_cost_slider.update_handle()
            
            self.castle_copper_cost_slider.value = self.castle_health_cost.get("Copper", 0)
            self.castle_copper_cost_slider.update_handle()
            
            self.castle_monster_coin_cost_slider.value = self.castle_health_cost.get("Monster Coins", 1)
            self.castle_monster_coin_cost_slider.update_handle()
            
        elif self.selected_upgrade_type == "damage_reduction":
            # Update multiplier slider
            self.castle_upgrade_multiplier_slider.value = self.castle_dr_mult
            self.castle_upgrade_multiplier_slider.update_handle()
            
            # Update cost sliders
            self.castle_stone_cost_slider.value = self.castle_dr_cost.get("Stone", 40)
            self.castle_stone_cost_slider.update_handle()
            
            self.castle_iron_cost_slider.value = self.castle_dr_cost.get("Iron", 15)
            self.castle_iron_cost_slider.update_handle()
            
            self.castle_copper_cost_slider.value = self.castle_dr_cost.get("Copper", 0)
            self.castle_copper_cost_slider.update_handle()
            
            self.castle_monster_coin_cost_slider.value = self.castle_dr_cost.get("Monster Coins", 2)
            self.castle_monster_coin_cost_slider.update_handle()
            
        elif self.selected_upgrade_type == "health_regen":
            # Update multiplier slider
            self.castle_upgrade_multiplier_slider.value = self.castle_regen_mult
            self.castle_upgrade_multiplier_slider.update_handle()
            
            # Update cost sliders
            self.castle_stone_cost_slider.value = self.castle_regen_cost.get("Stone", 30)
            self.castle_stone_cost_slider.update_handle()
            
            self.castle_iron_cost_slider.value = self.castle_regen_cost.get("Iron", 10)
            self.castle_iron_cost_slider.update_handle()
            
            self.castle_copper_cost_slider.value = self.castle_regen_cost.get("Copper", 5)
            self.castle_copper_cost_slider.update_handle()
            
            self.castle_monster_coin_cost_slider.value = self.castle_regen_cost.get("Monster Coins", 3)
            self.castle_monster_coin_cost_slider.update_handle()
    
    def _update_visible_sections(self):
        """Update which sections are visible based on selected building type"""
        # This implementation won't actually hide/show controls directly,
        # but instead will handle them differently in the draw() method
        # We'll still update sliders here for immediate feedback
        
        # When switching to another building type, refresh relevant sliders
        if self.selected_building_type == "Mine":
            self.mine_initial_production_slider.value = self.mine_initial_production
            self.mine_initial_production_slider.update_handle()
            
            self.mine_production_multiplier_slider.value = self.mine_production_multiplier
            self.mine_production_multiplier_slider.update_handle()
            
            self.mine_upgrade_time_multiplier_slider.value = self.mine_upgrade_time_multiplier
            self.mine_upgrade_time_multiplier_slider.update_handle()
            
            self.mine_initial_upgrade_time_slider.value = self.mine_initial_upgrade_time
            self.mine_initial_upgrade_time_slider.update_handle()
            
            self.mine_upgrade_cost_slider.value = self.mine_upgrade_cost.get("Boss Cores", 1)
            self.mine_upgrade_cost_slider.update_handle()
            
        elif self.selected_building_type == "Coresmith":
            self.coresmith_crafting_time_slider.value = self.coresmith_crafting_time
            self.coresmith_crafting_time_slider.update_handle()
            
        elif self.selected_building_type == "Castle":
            # Refresh castle sliders based on selected upgrade type
            self._castle_upgrade_type_selected(self.castle_upgrade_dropdown.selected_index)
    
    # Mine Settings Callbacks
    def _set_mine_initial_production(self, value):
        """Callback for mine initial production slider"""
        self.mine_initial_production = value
        # Update global mine initial production
        from config_extension import set_mine_initial_production
        set_mine_initial_production(value)
    
    def _set_mine_production_multiplier(self, value):
        """Callback for mine production multiplier slider"""
        self.mine_production_multiplier = value
        # Update global mine production multiplier
        from config_extension import set_mine_production_multiplier
        set_mine_production_multiplier(value)
    
    def _set_mine_upgrade_time_multiplier(self, value):
        """Callback for mine upgrade time multiplier slider"""
        self.mine_upgrade_time_multiplier = value
        # Update global mine upgrade time multiplier
        # Note: There doesn't appear to be a dedicated function in config_extension.py
        # for this, so we'd need to add one or modify directly
        # Update the module in sys.modules
        import sys
        module = sys.modules['config']
        module.MINE_UPGRADE_TIME_MULTIPLIER = value
    
    def _set_mine_initial_upgrade_time(self, value):
        """Callback for mine initial upgrade time slider"""
        self.mine_initial_upgrade_time = value
        # Update global mine initial upgrade time
        # Note: Similar to above, we'd need a dedicated function or direct modification
        import sys
        module = sys.modules['config']
        module.MINE_INITIAL_UPGRADE_TIME = value
    
    def _set_mine_upgrade_cost(self, value):
        """Callback for mine upgrade cost slider"""
        self.mine_upgrade_cost["Boss Cores"] = int(value)
        # Update global mine upgrade cost
        # We'd need a dedicated function or direct modification here as well
        import sys
        module = sys.modules['config']
        module.MINE_UPGRADE_COST = self.mine_upgrade_cost.copy()
    
    # Coresmith Settings Callbacks
    def _set_coresmith_crafting_time(self, value):
        """Callback for coresmith crafting time slider"""
        self.coresmith_crafting_time = value
        # Update global coresmith crafting time
        import sys
        module = sys.modules['config']
        module.CORESMITH_CRAFTING_TIME = value
    
    # Castle Settings Callbacks
    def _set_castle_upgrade_multiplier(self, value):
        """Callback for castle upgrade multiplier slider"""
        # Update the appropriate multiplier based on selected upgrade type
        if self.selected_upgrade_type == "health":
            self.castle_health_mult = value
            from config_extension import set_castle_health_upgrade_multiplier
            set_castle_health_upgrade_multiplier(value)
        elif self.selected_upgrade_type == "damage_reduction":
            self.castle_dr_mult = value
            from config_extension import set_castle_damage_reduction_upgrade_multiplier
            set_castle_damage_reduction_upgrade_multiplier(value)
        elif self.selected_upgrade_type == "health_regen":
            self.castle_regen_mult = value
            from config_extension import set_castle_health_regen_upgrade_multiplier
            set_castle_health_regen_upgrade_multiplier(value)
    
    def _set_castle_stone_cost(self, value):
        """Callback for castle stone cost slider"""
        # Update the appropriate cost based on selected upgrade type
        if self.selected_upgrade_type == "health":
            self.castle_health_cost["Stone"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Stone", int(value))
        elif self.selected_upgrade_type == "damage_reduction":
            self.castle_dr_cost["Stone"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Stone", int(value))
        elif self.selected_upgrade_type == "health_regen":
            self.castle_regen_cost["Stone"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Stone", int(value))
    
    def _set_castle_iron_cost(self, value):
        """Callback for castle iron cost slider"""
        # Update the appropriate cost based on selected upgrade type
        if self.selected_upgrade_type == "health":
            self.castle_health_cost["Iron"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Iron", int(value))
        elif self.selected_upgrade_type == "damage_reduction":
            self.castle_dr_cost["Iron"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Iron", int(value))
        elif self.selected_upgrade_type == "health_regen":
            self.castle_regen_cost["Iron"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Iron", int(value))
    
    def _set_castle_copper_cost(self, value):
        """Callback for castle copper cost slider"""
        # Update the appropriate cost based on selected upgrade type
        if self.selected_upgrade_type == "health":
            self.castle_health_cost["Copper"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Copper", int(value))
        elif self.selected_upgrade_type == "damage_reduction":
            self.castle_dr_cost["Copper"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Copper", int(value))
        elif self.selected_upgrade_type == "health_regen":
            self.castle_regen_cost["Copper"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Copper", int(value))
    
    def _set_castle_monster_coin_cost(self, value):
        """Callback for castle Monster Coin cost slider"""
        # Update the appropriate cost based on selected upgrade type
        if self.selected_upgrade_type == "health":
            self.castle_health_cost["Monster Coins"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health", "Monster Coins", int(value))
        elif self.selected_upgrade_type == "damage_reduction":
            self.castle_dr_cost["Monster Coins"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("damage_reduction", "Monster Coins", int(value))
        elif self.selected_upgrade_type == "health_regen":
            self.castle_regen_cost["Monster Coins"] = int(value)
            from config_extension import update_castle_upgrade_cost
            update_castle_upgrade_cost("health_regen", "Monster Coins", int(value))
    
    def reset(self):
        """Reset all building values to original values"""
        # Reset Mine settings
        self.mine_initial_production = self.original_mine_initial_production
        self.mine_production_multiplier = self.original_mine_production_multiplier
        self.mine_upgrade_time_multiplier = self.original_mine_upgrade_time_multiplier
        self.mine_initial_upgrade_time = self.original_mine_initial_upgrade_time
        self.mine_upgrade_cost = self.original_mine_upgrade_cost.copy()
        
        # Reset Coresmith settings
        self.coresmith_crafting_time = self.original_coresmith_crafting_time
        
        # Reset Castle settings
        self.castle_health_cost = self.original_castle_health_cost.copy()
        self.castle_dr_cost = self.original_castle_dr_cost.copy()
        self.castle_regen_cost = self.original_castle_regen_cost.copy()
        self.castle_health_mult = self.original_castle_health_mult
        self.castle_dr_mult = self.original_castle_dr_mult
        self.castle_regen_mult = self.original_castle_regen_mult
        
        # Update global values
        from config_extension import (
            set_mine_initial_production,
            set_mine_production_multiplier,
            reset_castle_upgrade_costs,
            set_castle_health_upgrade_multiplier,
            set_castle_damage_reduction_upgrade_multiplier,
            set_castle_health_regen_upgrade_multiplier
        )
        
        # Update Mine settings
        set_mine_initial_production(self.original_mine_initial_production)
        set_mine_production_multiplier(self.original_mine_production_multiplier)
        
        # Update module values directly for values without dedicated functions
        import sys
        module = sys.modules['config']
        module.MINE_UPGRADE_TIME_MULTIPLIER = self.original_mine_upgrade_time_multiplier
        module.MINE_INITIAL_UPGRADE_TIME = self.original_mine_initial_upgrade_time
        module.MINE_UPGRADE_COST = self.original_mine_upgrade_cost.copy()
        module.CORESMITH_CRAFTING_TIME = self.original_coresmith_crafting_time
        
        # Reset Castle settings
        reset_castle_upgrade_costs()
        set_castle_health_upgrade_multiplier(self.original_castle_health_mult)
        set_castle_damage_reduction_upgrade_multiplier(self.original_castle_dr_mult)
        set_castle_health_regen_upgrade_multiplier(self.original_castle_regen_mult)
        
        # Reset control values
        for control in self.controls:
            if hasattr(control, 'reset'):
                control.reset()
        
        # Update based on current selected type
        self._update_visible_sections()
    
    def draw(self, screen):
        """Draw the tab and its controls"""
        # Draw the background
        super().draw(screen)
        
        # Draw title
        title_text = "Buildings Balance"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_rect = title_surface.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title_surface, title_rect)
        
        # Always draw building type dropdown
        self.building_type_dropdown.draw(screen)
        
        # Draw appropriate section based on selected building type
        if self.selected_building_type == "Mine":
            # Draw Mine section header
            y_pos = self.mine_section_y
            section_text = "Mine Settings"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, y_pos))
            
            # Draw Mine controls
            self.mine_initial_production_slider.draw(screen)
            self.mine_production_multiplier_slider.draw(screen)
            self.mine_upgrade_time_multiplier_slider.draw(screen)
            self.mine_initial_upgrade_time_slider.draw(screen)
            self.mine_upgrade_cost_slider.draw(screen)
            
        elif self.selected_building_type == "Coresmith":
            # Draw Coresmith section header
            y_pos = self.coresmith_section_y
            section_text = "Coresmith Settings"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, y_pos))
            
            # Draw Coresmith controls
            self.coresmith_crafting_time_slider.draw(screen)
            
        elif self.selected_building_type == "Castle":
            # Draw Castle section header
            y_pos = self.castle_section_y
            section_text = "Castle Settings"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, y_pos))
            
            # Draw Castle controls
            self.castle_upgrade_dropdown.draw(screen)
            self.castle_upgrade_multiplier_slider.draw(screen)
            self.castle_stone_cost_slider.draw(screen)
            self.castle_iron_cost_slider.draw(screen)
            self.castle_copper_cost_slider.draw(screen)
            self.castle_monster_coin_cost_slider.draw(screen)
        
        # Always draw reset button
        self.controls[-1].draw(screen)
