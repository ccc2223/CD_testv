# ui/dev_menu/tower_tab.py
"""
Tower upgrade tab for developer menu
"""
import pygame
import copy
from .components import Tab, Slider, Button, DropdownMenu
from config import (
    TOWER_TYPES,
    TOWER_MONSTER_COIN_COSTS,
    TOWER_UPGRADE_COST_MULTIPLIER,
    TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
    TOWER_DAMAGE_UPGRADE_MULTIPLIER,
    TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER,
    TOWER_RANGE_UPGRADE_MULTIPLIER,
    TOWER_AOE_UPGRADE_MULTIPLIER
)

class TowerUpgradeTab(Tab):
    """Tab for adjusting tower upgrade costs"""
    def __init__(self, rect, game_instance):
        """
        Initialize tower upgrade tab
        
        Args:
            rect: Pygame Rect defining the tab area
            game_instance: Reference to the Game instance
        """
        super().__init__(rect)
        self.game = game_instance
        
        # Store original values for reset
        self.original_upgrade_cost_multiplier = TOWER_UPGRADE_COST_MULTIPLIER
        self.original_monster_coin_upgrade_multiplier = TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER
        self.original_damage_upgrade_multiplier = TOWER_DAMAGE_UPGRADE_MULTIPLIER
        self.original_attack_speed_upgrade_multiplier = TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER
        self.original_range_upgrade_multiplier = TOWER_RANGE_UPGRADE_MULTIPLIER
        self.original_aoe_upgrade_multiplier = TOWER_AOE_UPGRADE_MULTIPLIER
        self.original_tower_types = {
            tower_type: tower_data.copy() for tower_type, tower_data in TOWER_TYPES.items()
        }
        self.original_tower_monster_coin_costs = TOWER_MONSTER_COIN_COSTS.copy()
        
        # Local copies of values that we'll modify
        self.upgrade_cost_multiplier = TOWER_UPGRADE_COST_MULTIPLIER
        self.monster_coin_upgrade_multiplier = TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER
        self.damage_upgrade_multiplier = TOWER_DAMAGE_UPGRADE_MULTIPLIER
        self.attack_speed_upgrade_multiplier = TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER
        self.range_upgrade_multiplier = TOWER_RANGE_UPGRADE_MULTIPLIER
        self.aoe_upgrade_multiplier = TOWER_AOE_UPGRADE_MULTIPLIER
        self.tower_types = {
            tower_type: tower_data.copy() for tower_type, tower_data in TOWER_TYPES.items()
        }
        self.tower_monster_coin_costs = TOWER_MONSTER_COIN_COSTS.copy()
        
        # Custom resource costs for different upgrade types
        # Structure: {tower_type: {upgrade_type: {resource: cost}}}
        # Default will use the regular tower costs if not specified
        self.upgrade_resource_costs = {}
        for tower_type in TOWER_TYPES:
            self.upgrade_resource_costs[tower_type] = {}
            for upgrade_type in ["damage", "attack_speed", "range"]:
                # Start with costs from tower_types
                self.upgrade_resource_costs[tower_type][upgrade_type] = {}
        
        # Initialize with default costs for all tower types and upgrade types
        for tower_type, tower_data in self.tower_types.items():
            if "cost" in tower_data:
                for upgrade_type in ["damage", "attack_speed", "range"]:
                    self.upgrade_resource_costs[tower_type][upgrade_type] = tower_data["cost"].copy()
        
        # Upgrade type options
        self.upgrade_types = ["Base Stats", "Damage", "Attack Speed", "Range", "Special"]
        self.current_upgrade_type = "Base Stats"
        
        # Initialize controls
        self._init_controls()
    
    def _init_controls(self):
        """Initialize all controls for this tab"""
        y_pos = self.rect.top + 20
        width = self.rect.width - 40
        
        # Title
        title_text = "Tower Upgrade Costs"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_pos = (self.rect.left + 20, y_pos)
        y_pos += 30
        
        # Tower type dropdown
        tower_types = list(self.tower_types.keys())
        self.tower_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Tower Type:",
            tower_types,
            0,
            self._tower_type_selected
        )
        self.controls.append(self.tower_dropdown)
        y_pos += 30
        
        # Upgrade type dropdown
        self.upgrade_type_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Upgrade Type:",
            self.upgrade_types,
            0,
            self._upgrade_type_selected
        )
        self.controls.append(self.upgrade_type_dropdown)
        y_pos += 40
        
        # Section: Base Stats
        self.base_stats_section_y = y_pos
        section_text = "Base Tower Stats"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Base Stats Controls
        # Tower damage slider
        self.damage_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Base Damage:",
            self.tower_types["Archer"]["damage"],
            5,
            100,
            5,
            self._set_tower_damage,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.damage_slider)
        y_pos += 30
        
        # Tower attack speed slider
        self.attack_speed_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Attack Speed:",
            self.tower_types["Archer"]["attack_speed"],
            0.1,
            3.0,
            0.1,
            self._set_tower_attack_speed
        )
        self.controls.append(self.attack_speed_slider)
        y_pos += 30
        
        # Tower range slider
        self.range_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Range:",
            self.tower_types["Archer"]["range"],
            50,
            400,
            10,
            self._set_tower_range,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.range_slider)
        y_pos += 30
        
        # Tower base monster coin cost
        self.monster_coin_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Monster Coin Cost:",
            self.tower_monster_coin_costs.get("Archer", 5),
            1,
            30,
            1,
            self._set_tower_monster_coin_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.monster_coin_cost_slider)
        y_pos += 40
        
        # Section: Base Resource Costs
        self.resource_costs_section_y = y_pos
        section_text = "Base Resource Costs"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Tower stone cost slider
        self.stone_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Stone Cost:",
            self.tower_types["Archer"]["cost"].get("Stone", 20),
            10,
            100,
            5,
            self._set_tower_stone_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.stone_cost_slider)
        y_pos += 30
        
        # Tower iron cost slider
        self.iron_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Iron Cost:",
            self.tower_types["Archer"]["cost"].get("Iron", 0),
            0,
            50,
            5,
            self._set_tower_iron_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.iron_cost_slider)
        y_pos += 30
        
        # Tower copper cost slider
        self.copper_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Copper Cost:",
            self.tower_types["Archer"]["cost"].get("Copper", 0),
            0,
            25,
            1,
            self._set_tower_copper_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.copper_cost_slider)
        y_pos += 30
        
        # Tower thorium cost slider
        self.thorium_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Thorium Cost:",
            self.tower_types["Archer"]["cost"].get("Thorium", 0),
            0,
            10,
            1,
            self._set_tower_thorium_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.thorium_cost_slider)
        y_pos += 40
        
        # Section: Upgrade-specific resource costs
        self.upgrade_costs_section_y = y_pos
        section_text = "Upgrade-Specific Resource Costs"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Upgrade stone cost slider
        self.upgrade_stone_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Stone Cost:",
            0,
            0,
            100,
            5,
            self._set_upgrade_stone_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.upgrade_stone_cost_slider)
        y_pos += 30
        
        # Upgrade iron cost slider
        self.upgrade_iron_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Iron Cost:",
            0,
            0,
            50,
            5,
            self._set_upgrade_iron_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.upgrade_iron_cost_slider)
        y_pos += 30
        
        # Upgrade copper cost slider
        self.upgrade_copper_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Copper Cost:",
            0,
            0,
            25,
            1,
            self._set_upgrade_copper_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.upgrade_copper_cost_slider)
        y_pos += 30
        
        # Upgrade thorium cost slider
        self.upgrade_thorium_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Thorium Cost:",
            0,
            0,
            10,
            1,
            self._set_upgrade_thorium_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.upgrade_thorium_cost_slider)
        y_pos += 30
        
        # Upgrade monster coins cost slider
        self.upgrade_monster_coins_cost_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Monster Coins Cost:",
            5,
            0,
            30,
            1,
            self._set_upgrade_monster_coins_cost,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.upgrade_monster_coins_cost_slider)
        y_pos += 40
        
        # Section: Upgrade Multipliers
        self.multipliers_section_y = y_pos
        section_text = "Upgrade Multipliers"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Global upgrade cost multiplier
        self.upgrade_cost_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Resource Cost Multiplier:",
            self.upgrade_cost_multiplier,
            1.1,
            2.0,
            0.1,
            self._set_upgrade_cost_multiplier
        )
        self.controls.append(self.upgrade_cost_multiplier_slider)
        y_pos += 30
        
        # Global Monster Coin upgrade multiplier
        self.monster_coin_upgrade_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Monster Coin Multiplier:",
            self.monster_coin_upgrade_multiplier,
            1.1,
            2.0,
            0.1,
            self._set_monster_coin_upgrade_multiplier
        )
        self.controls.append(self.monster_coin_upgrade_multiplier_slider)
        y_pos += 30
        
        # Damage upgrade multiplier
        self.damage_upgrade_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Damage Upgrade Multiplier:",
            self.damage_upgrade_multiplier,
            1.1,
            1.5,
            0.05,
            self._set_damage_upgrade_multiplier
        )
        self.controls.append(self.damage_upgrade_multiplier_slider)
        y_pos += 30
        
        # Attack speed upgrade multiplier
        self.attack_speed_upgrade_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Speed Upgrade Multiplier:",
            self.attack_speed_upgrade_multiplier,
            1.05,
            1.4,
            0.05,
            self._set_attack_speed_upgrade_multiplier
        )
        self.controls.append(self.attack_speed_upgrade_multiplier_slider)
        y_pos += 30
        
        # Range upgrade multiplier
        self.range_upgrade_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Range Upgrade Multiplier:",
            self.range_upgrade_multiplier,
            1.05,
            1.4,
            0.05,
            self._set_range_upgrade_multiplier
        )
        self.controls.append(self.range_upgrade_multiplier_slider)
        y_pos += 30
        
        # AOE upgrade multiplier
        self.aoe_upgrade_multiplier_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "AOE Upgrade Multiplier:",
            self.aoe_upgrade_multiplier,
            1.05,
            1.4,
            0.05,
            self._set_aoe_upgrade_multiplier
        )
        self.controls.append(self.aoe_upgrade_multiplier_slider)
        y_pos += 40
        
        # Reset button
        reset_button = Button(
            (self.rect.centerx - 60, self.rect.bottom - 40),
            (120, 30),
            "Reset to Defaults",
            self.reset
        )
        self.controls.append(reset_button)
        
        # Update control visibility based on selected upgrade type
        self._update_section_visibility()
    
    def _update_section_visibility(self):
        """Update control visibility based on selected upgrade type"""
        # Base Stats Controls
        base_stats_controls = [
            self.damage_slider,
            self.attack_speed_slider,
            self.range_slider,
            self.monster_coin_cost_slider
        ]
        
        # Resource Costs Controls
        resource_costs_controls = [
            self.stone_cost_slider,
            self.iron_cost_slider,
            self.copper_cost_slider,
            self.thorium_cost_slider
        ]
        
        # Upgrade Resource Costs Controls
        upgrade_costs_controls = [
            self.upgrade_stone_cost_slider,
            self.upgrade_iron_cost_slider,
            self.upgrade_copper_cost_slider,
            self.upgrade_thorium_cost_slider,
            self.upgrade_monster_coins_cost_slider
        ]
        
        # Multiplier Controls (always visible)
        multiplier_controls = [
            self.upgrade_cost_multiplier_slider,
            self.monster_coin_upgrade_multiplier_slider,
            self.damage_upgrade_multiplier_slider,
            self.attack_speed_upgrade_multiplier_slider,
            self.range_upgrade_multiplier_slider,
            self.aoe_upgrade_multiplier_slider
        ]
        
        # Hide or show controls based on selected upgrade type
        for control in base_stats_controls:
            control.visible = (self.current_upgrade_type == "Base Stats")
        
        for control in resource_costs_controls:
            control.visible = (self.current_upgrade_type == "Base Stats")
        
        for control in upgrade_costs_controls:
            control.visible = (self.current_upgrade_type in ["Damage", "Attack Speed", "Range", "Special"])
    
    def _tower_type_selected(self, index):
        """Callback for tower type dropdown"""
        tower_type = list(self.tower_types.keys())[index]
        tower_data = self.tower_types[tower_type]
        
        # Update based on current upgrade type
        if self.current_upgrade_type == "Base Stats":
            # Update base stats sliders
            self.damage_slider.value = tower_data["damage"]
            self.damage_slider.update_handle()
            
            self.attack_speed_slider.value = tower_data["attack_speed"]
            self.attack_speed_slider.update_handle()
            
            self.range_slider.value = tower_data["range"]
            self.range_slider.update_handle()
            
            self.monster_coin_cost_slider.value = self.tower_monster_coin_costs.get(tower_type, 5)
            self.monster_coin_cost_slider.update_handle()
            
            # Update resource cost sliders
            if "cost" in tower_data:
                self.stone_cost_slider.value = tower_data["cost"].get("Stone", 0)
                self.stone_cost_slider.update_handle()
                
                self.iron_cost_slider.value = tower_data["cost"].get("Iron", 0)
                self.iron_cost_slider.update_handle()
                
                self.copper_cost_slider.value = tower_data["cost"].get("Copper", 0)
                self.copper_cost_slider.update_handle()
                
                self.thorium_cost_slider.value = tower_data["cost"].get("Thorium", 0)
                self.thorium_cost_slider.update_handle()
        else:
            # Get upgrade type
            upgrade_type = self.current_upgrade_type.lower().replace(" ", "_")
            
            # Update upgrade-specific resource costs
            if tower_type in self.upgrade_resource_costs and upgrade_type in self.upgrade_resource_costs[tower_type]:
                costs = self.upgrade_resource_costs[tower_type][upgrade_type]
                
                self.upgrade_stone_cost_slider.value = costs.get("Stone", 0)
                self.upgrade_stone_cost_slider.update_handle()
                
                self.upgrade_iron_cost_slider.value = costs.get("Iron", 0)
                self.upgrade_iron_cost_slider.update_handle()
                
                self.upgrade_copper_cost_slider.value = costs.get("Copper", 0)
                self.upgrade_copper_cost_slider.update_handle()
                
                self.upgrade_thorium_cost_slider.value = costs.get("Thorium", 0)
                self.upgrade_thorium_cost_slider.update_handle()
                
                self.upgrade_monster_coins_cost_slider.value = costs.get("Monster Coins", 0)
                self.upgrade_monster_coins_cost_slider.update_handle()
    
    def _upgrade_type_selected(self, index):
        """Callback for upgrade type dropdown"""
        self.current_upgrade_type = self.upgrade_types[index]
        self._update_section_visibility()
        
        # Update sliders based on current tower and upgrade type
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        self._tower_type_selected(self.tower_dropdown.selected_index)
    
    def _set_tower_damage(self, value):
        """Callback for tower damage slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower damage
        self.tower_types[tower_type]["damage"] = int(value)
        # Update global tower stats
        from config_extension import update_tower_stat
        update_tower_stat(tower_type, "damage", int(value))
    
    def _set_tower_attack_speed(self, value):
        """Callback for tower attack speed slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower attack speed
        self.tower_types[tower_type]["attack_speed"] = value
        # Update global tower stats
        from config_extension import update_tower_stat
        update_tower_stat(tower_type, "attack_speed", value)
    
    def _set_tower_range(self, value):
        """Callback for tower range slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower range
        self.tower_types[tower_type]["range"] = int(value)
        # Update global tower stats
        from config_extension import update_tower_stat
        update_tower_stat(tower_type, "range", int(value))
    
    def _set_tower_monster_coin_cost(self, value):
        """Callback for tower Monster Coin cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower Monster Coin cost
        self.tower_monster_coin_costs[tower_type] = int(value)
        # Update global tower Monster Coin costs
        from config_extension import update_tower_monster_coin_cost
        update_tower_monster_coin_cost(tower_type, int(value))
    
    def _set_tower_stone_cost(self, value):
        """Callback for tower stone cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower stone cost
        if "cost" not in self.tower_types[tower_type]:
            self.tower_types[tower_type]["cost"] = {}
        self.tower_types[tower_type]["cost"]["Stone"] = int(value)
        # Update global tower costs
        from config_extension import update_tower_cost
        update_tower_cost(tower_type, "Stone", int(value))
    
    def _set_tower_iron_cost(self, value):
        """Callback for tower iron cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower iron cost
        if "cost" not in self.tower_types[tower_type]:
            self.tower_types[tower_type]["cost"] = {}
        self.tower_types[tower_type]["cost"]["Iron"] = int(value)
        # Update global tower costs
        from config_extension import update_tower_cost
        update_tower_cost(tower_type, "Iron", int(value))
    
    def _set_tower_copper_cost(self, value):
        """Callback for tower copper cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower copper cost
        if "cost" not in self.tower_types[tower_type]:
            self.tower_types[tower_type]["cost"] = {}
        self.tower_types[tower_type]["cost"]["Copper"] = int(value)
        # Update global tower costs
        from config_extension import update_tower_cost
        update_tower_cost(tower_type, "Copper", int(value))
    
    def _set_tower_thorium_cost(self, value):
        """Callback for tower thorium cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        # Update tower thorium cost
        if "cost" not in self.tower_types[tower_type]:
            self.tower_types[tower_type]["cost"] = {}
        self.tower_types[tower_type]["cost"]["Thorium"] = int(value)
        # Update global tower costs
        from config_extension import update_tower_cost
        update_tower_cost(tower_type, "Thorium", int(value))
    
    def _set_upgrade_stone_cost(self, value):
        """Callback for upgrade stone cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        upgrade_type = self.current_upgrade_type.lower().replace(" ", "_")
        
        # Skip for base stats (uses regular cost sliders)
        if upgrade_type == "base_stats":
            return
            
        # Handle special case for special upgrades
        if upgrade_type == "special":
            if tower_type == "Splash":
                upgrade_type = "aoe_radius"
            elif tower_type == "Frozen":
                upgrade_type = "slow_effect"
            else:
                # No special upgrade for other towers
                return
        
        # Update upgrade-specific cost
        if tower_type not in self.upgrade_resource_costs:
            self.upgrade_resource_costs[tower_type] = {}
        
        if upgrade_type not in self.upgrade_resource_costs[tower_type]:
            self.upgrade_resource_costs[tower_type][upgrade_type] = {}
        
        self.upgrade_resource_costs[tower_type][upgrade_type]["Stone"] = int(value)
        
        # Store these custom costs in a way that base_tower.py can access
        # We'll update a global in the config module
        module = __import__('sys').modules['config']
        if not hasattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS'):
            module.TOWER_UPGRADE_RESOURCE_COSTS = {}
        
        if tower_type not in module.TOWER_UPGRADE_RESOURCE_COSTS:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type] = {}
            
        if upgrade_type not in module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type]:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type] = {}
        
        module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type]["Stone"] = int(value)
    
    def _set_upgrade_iron_cost(self, value):
        """Callback for upgrade iron cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        upgrade_type = self.current_upgrade_type.lower().replace(" ", "_")
        
        # Skip for base stats (uses regular cost sliders)
        if upgrade_type == "base_stats":
            return
            
        # Handle special case for special upgrades
        if upgrade_type == "special":
            if tower_type == "Splash":
                upgrade_type = "aoe_radius"
            elif tower_type == "Frozen":
                upgrade_type = "slow_effect"
            else:
                # No special upgrade for other towers
                return
        
        # Update upgrade-specific cost
        if tower_type not in self.upgrade_resource_costs:
            self.upgrade_resource_costs[tower_type] = {}
        
        if upgrade_type not in self.upgrade_resource_costs[tower_type]:
            self.upgrade_resource_costs[tower_type][upgrade_type] = {}
        
        self.upgrade_resource_costs[tower_type][upgrade_type]["Iron"] = int(value)
        
        # Store these custom costs in a way that base_tower.py can access
        module = __import__('sys').modules['config']
        if not hasattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS'):
            module.TOWER_UPGRADE_RESOURCE_COSTS = {}
        
        if tower_type not in module.TOWER_UPGRADE_RESOURCE_COSTS:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type] = {}
            
        if upgrade_type not in module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type]:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type] = {}
        
        module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type]["Iron"] = int(value)
    
    def _set_upgrade_copper_cost(self, value):
        """Callback for upgrade copper cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        upgrade_type = self.current_upgrade_type.lower().replace(" ", "_")
        
        # Skip for base stats (uses regular cost sliders)
        if upgrade_type == "base_stats":
            return
            
        # Handle special case for special upgrades
        if upgrade_type == "special":
            if tower_type == "Splash":
                upgrade_type = "aoe_radius"
            elif tower_type == "Frozen":
                upgrade_type = "slow_effect"
            else:
                # No special upgrade for other towers
                return
        
        # Update upgrade-specific cost
        if tower_type not in self.upgrade_resource_costs:
            self.upgrade_resource_costs[tower_type] = {}
        
        if upgrade_type not in self.upgrade_resource_costs[tower_type]:
            self.upgrade_resource_costs[tower_type][upgrade_type] = {}
        
        self.upgrade_resource_costs[tower_type][upgrade_type]["Copper"] = int(value)
        
        # Store these custom costs in a way that base_tower.py can access
        module = __import__('sys').modules['config']
        if not hasattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS'):
            module.TOWER_UPGRADE_RESOURCE_COSTS = {}
        
        if tower_type not in module.TOWER_UPGRADE_RESOURCE_COSTS:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type] = {}
            
        if upgrade_type not in module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type]:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type] = {}
        
        module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type]["Copper"] = int(value)
    
    def _set_upgrade_thorium_cost(self, value):
        """Callback for upgrade thorium cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        upgrade_type = self.current_upgrade_type.lower().replace(" ", "_")
        
        # Skip for base stats (uses regular cost sliders)
        if upgrade_type == "base_stats":
            return
            
        # Handle special case for special upgrades
        if upgrade_type == "special":
            if tower_type == "Splash":
                upgrade_type = "aoe_radius"
            elif tower_type == "Frozen":
                upgrade_type = "slow_effect"
            else:
                # No special upgrade for other towers
                return
        
        # Update upgrade-specific cost
        if tower_type not in self.upgrade_resource_costs:
            self.upgrade_resource_costs[tower_type] = {}
        
        if upgrade_type not in self.upgrade_resource_costs[tower_type]:
            self.upgrade_resource_costs[tower_type][upgrade_type] = {}
        
        self.upgrade_resource_costs[tower_type][upgrade_type]["Thorium"] = int(value)
        
        # Store these custom costs in a way that base_tower.py can access
        module = __import__('sys').modules['config']
        if not hasattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS'):
            module.TOWER_UPGRADE_RESOURCE_COSTS = {}
        
        if tower_type not in module.TOWER_UPGRADE_RESOURCE_COSTS:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type] = {}
            
        if upgrade_type not in module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type]:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type] = {}
        
        module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type]["Thorium"] = int(value)
    
    def _set_upgrade_monster_coins_cost(self, value):
        """Callback for upgrade monster coins cost slider"""
        tower_type = list(self.tower_types.keys())[self.tower_dropdown.selected_index]
        upgrade_type = self.current_upgrade_type.lower().replace(" ", "_")
        
        # Skip for base stats (uses regular cost sliders)
        if upgrade_type == "base_stats":
            return
            
        # Handle special case for special upgrades
        if upgrade_type == "special":
            if tower_type == "Splash":
                upgrade_type = "aoe_radius"
            elif tower_type == "Frozen":
                upgrade_type = "slow_effect"
            else:
                # No special upgrade for other towers
                return
        
        # Update upgrade-specific cost
        if tower_type not in self.upgrade_resource_costs:
            self.upgrade_resource_costs[tower_type] = {}
        
        if upgrade_type not in self.upgrade_resource_costs[tower_type]:
            self.upgrade_resource_costs[tower_type][upgrade_type] = {}
        
        self.upgrade_resource_costs[tower_type][upgrade_type]["Monster Coins"] = int(value)
        
        # Store these custom costs in a way that base_tower.py can access
        module = __import__('sys').modules['config']
        if not hasattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS'):
            module.TOWER_UPGRADE_RESOURCE_COSTS = {}
        
        if tower_type not in module.TOWER_UPGRADE_RESOURCE_COSTS:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type] = {}
            
        if upgrade_type not in module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type]:
            module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type] = {}
        
        module.TOWER_UPGRADE_RESOURCE_COSTS[tower_type][upgrade_type]["Monster Coins"] = int(value)
    
    def _set_upgrade_cost_multiplier(self, value):
        """Callback for upgrade cost multiplier slider"""
        self.upgrade_cost_multiplier = value
        # Update global upgrade cost multiplier
        from config_extension import set_tower_upgrade_cost_multiplier
        set_tower_upgrade_cost_multiplier(value)
    
    def _set_monster_coin_upgrade_multiplier(self, value):
        """Callback for Monster Coin upgrade multiplier slider"""
        self.monster_coin_upgrade_multiplier = value
        # Update global Monster Coin upgrade multiplier
        from config_extension import set_tower_monster_coin_upgrade_multiplier
        set_tower_monster_coin_upgrade_multiplier(value)
    
    def _set_damage_upgrade_multiplier(self, value):
        """Callback for damage upgrade multiplier slider"""
        self.damage_upgrade_multiplier = value
        # Update global damage upgrade multiplier
        from config_extension import set_tower_damage_upgrade_multiplier
        set_tower_damage_upgrade_multiplier(value)
    
    def _set_attack_speed_upgrade_multiplier(self, value):
        """Callback for attack speed upgrade multiplier slider"""
        self.attack_speed_upgrade_multiplier = value
        # Update global attack speed upgrade multiplier
        from config_extension import set_tower_attack_speed_upgrade_multiplier
        set_tower_attack_speed_upgrade_multiplier(value)
    
    def _set_range_upgrade_multiplier(self, value):
        """Callback for range upgrade multiplier slider"""
        self.range_upgrade_multiplier = value
        # Update global range upgrade multiplier
        from config_extension import set_tower_range_upgrade_multiplier
        set_tower_range_upgrade_multiplier(value)
    
    def _set_aoe_upgrade_multiplier(self, value):
        """Callback for AOE upgrade multiplier slider"""
        self.aoe_upgrade_multiplier = value
        # Update global AOE upgrade multiplier
        module = __import__('sys').modules['config']
        module.TOWER_AOE_UPGRADE_MULTIPLIER = value
    
    def reset(self):
        """Reset all tower values to original values"""
        # Reset upgrade cost multiplier
        from config_extension import (
            set_tower_upgrade_cost_multiplier,
            set_tower_monster_coin_upgrade_multiplier,
            set_tower_damage_upgrade_multiplier,
            set_tower_attack_speed_upgrade_multiplier,
            set_tower_range_upgrade_multiplier
        )
        set_tower_upgrade_cost_multiplier(self.original_upgrade_cost_multiplier)
        set_tower_monster_coin_upgrade_multiplier(self.original_monster_coin_upgrade_multiplier)
        set_tower_damage_upgrade_multiplier(self.original_damage_upgrade_multiplier)
        set_tower_attack_speed_upgrade_multiplier(self.original_attack_speed_upgrade_multiplier)
        set_tower_range_upgrade_multiplier(self.original_range_upgrade_multiplier)
        
        # Reset AOE upgrade multiplier
        module = __import__('sys').modules['config']
        module.TOWER_AOE_UPGRADE_MULTIPLIER = self.original_aoe_upgrade_multiplier
        
        # Reset tower types
        for tower_type, tower_data in self.original_tower_types.items():
            # Reset tower costs
            if "cost" in tower_data:
                for resource, amount in tower_data["cost"].items():
                    from config_extension import update_tower_cost
                    update_tower_cost(tower_type, resource, amount)
            
            # Reset tower stats
            for stat, value in tower_data.items():
                if stat != "cost":
                    from config_extension import update_tower_stat
                    update_tower_stat(tower_type, stat, value)
        
        # Reset tower Monster Coin costs
        for tower_type, amount in self.original_tower_monster_coin_costs.items():
            from config_extension import update_tower_monster_coin_cost
            update_tower_monster_coin_cost(tower_type, amount)
        
        # Reset custom upgrade resource costs
        if hasattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS'):
            delattr(module, 'TOWER_UPGRADE_RESOURCE_COSTS')
        
        # Reset local values
        self.upgrade_cost_multiplier = self.original_upgrade_cost_multiplier
        self.monster_coin_upgrade_multiplier = self.original_monster_coin_upgrade_multiplier
        self.damage_upgrade_multiplier = self.original_damage_upgrade_multiplier
        self.attack_speed_upgrade_multiplier = self.original_attack_speed_upgrade_multiplier
        self.range_upgrade_multiplier = self.original_range_upgrade_multiplier
        self.aoe_upgrade_multiplier = self.original_aoe_upgrade_multiplier
        self.tower_types = {
            tower_type: tower_data.copy() for tower_type, tower_data in self.original_tower_types.items()
        }
        self.tower_monster_coin_costs = self.original_tower_monster_coin_costs.copy()
        
        # Reset upgrade resource costs
        self.upgrade_resource_costs = {}
        for tower_type in self.tower_types:
            self.upgrade_resource_costs[tower_type] = {}
            for upgrade_type in ["damage", "attack_speed", "range"]:
                self.upgrade_resource_costs[tower_type][upgrade_type] = {}
                
                # Initialize with costs from tower_types
                if "cost" in self.tower_types[tower_type]:
                    self.upgrade_resource_costs[tower_type][upgrade_type] = self.tower_types[tower_type]["cost"].copy()
        
        # Update sliders with default values
        for control in self.controls:
            if hasattr(control, 'reset'):
                control.reset()
                
        # Update currently selected tower type sliders
        self._upgrade_type_selected(self.upgrade_type_dropdown.selected_index)
        self._tower_type_selected(self.tower_dropdown.selected_index)
    
    def draw(self, screen):
        """Draw the tab and its controls"""
        super().draw(screen)
        
        # Draw title
        title_text = "Tower Upgrade Costs"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_rect = title_surface.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title_surface, title_rect)
        
        # Draw section headers based on current upgrade type
        if self.current_upgrade_type == "Base Stats":
            # Draw base stats section
            section_text = "Base Tower Stats"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, self.base_stats_section_y))
            
            # Draw resource costs section
            section_text = "Base Resource Costs"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, self.resource_costs_section_y))
        else:
            # Draw upgrade-specific costs section
            upgrade_type = self.current_upgrade_type
            section_text = f"{upgrade_type} Upgrade Resource Costs"
            section_surface = self.font.render(section_text, True, (200, 200, 255))
            screen.blit(section_surface, (self.rect.left + 20, self.upgrade_costs_section_y))
        
        # Always draw multipliers section
        section_text = "Upgrade Multipliers"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, self.multipliers_section_y))
