# ui/dev_menu/monster_tab.py
"""
Monster balance tab for developer menu
"""
import pygame
from .components import Tab, Slider, Button, DropdownMenu
from config import MONSTER_STATS, BOSS_STATS

class MonsterBalanceTab(Tab):
    """Tab for adjusting monster balance"""
    def __init__(self, rect, game_instance):
        """
        Initialize monster balance tab
        
        Args:
            rect: Pygame Rect defining the tab area
            game_instance: Reference to the Game instance
        """
        super().__init__(rect)
        self.game = game_instance
        
        # Store original values for reset
        self.original_monster_stats = {
            monster_type: stats.copy() for monster_type, stats in MONSTER_STATS.items()
        }
        self.original_boss_stats = {
            boss_type: stats.copy() for boss_type, stats in BOSS_STATS.items()
        }
        
        # Local copies of stats that we'll modify
        self.monster_stats = {
            monster_type: stats.copy() for monster_type, stats in MONSTER_STATS.items()
        }
        self.boss_stats = {
            boss_type: stats.copy() for boss_type, stats in BOSS_STATS.items()
        }
        
        # Monster-specific scaling factors (not in the original config)
        # Structure: {monster_type: {"health_scaling": value, "speed_scaling": value, "damage_scaling": value}}
        self.monster_scaling = {}
        for monster_type in MONSTER_STATS:
            self.monster_scaling[monster_type] = {
                "health_scaling": 1.2,  # Default to global scaling
                "speed_scaling": 1.0,   # By default speeds don't scale
                "damage_scaling": 1.2   # Default to global scaling
            }
        
        # Initialize controls
        self._init_controls()
    
    def _init_controls(self):
        """Initialize all controls for this tab"""
        y_pos = self.rect.top + 20
        width = self.rect.width - 40
        
        # Title
        title_text = "Monster Balance"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_pos = (self.rect.left + 20, y_pos)
        y_pos += 30
        
        # Section: Global Monster Scaling
        section_text = "Global Monster Scaling"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Wave difficulty multiplier
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Wave Difficulty Multiplier:",
            1.2,  # Default value from config
            1.0,
            1.5,
            0.05,
            self._set_wave_difficulty_multiplier
        ))
        y_pos += 30
        
        # Monster spawn interval
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Spawn Interval (seconds):",
            1.5,  # Default value from config
            0.5,
            3.0,
            0.1,
            self._set_monster_spawn_interval
        ))
        y_pos += 30
        
        # Base monsters per wave
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Base Monsters Per Wave:",
            5,  # Default value from config
            3,
            10,
            1,
            self._set_base_monsters_per_wave,
            lambda x: f"{int(x)}"
        ))
        y_pos += 30
        
        # Wave monster count multiplier
        self.controls.append(Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Wave Count Multiplier:",
            1.5,  # Default value from config
            1.0,
            2.0,
            0.1,
            self._set_wave_monster_count_multiplier
        ))
        y_pos += 40
        
        # Section: Monster Type Adjustments
        section_text = "Monster Type Adjustments"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Monster type dropdown
        monster_types = list(self.monster_stats.keys())
        self.monster_type_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Monster Type:",
            monster_types,
            0,
            self._monster_type_selected
        )
        self.controls.append(self.monster_type_dropdown)
        y_pos += 30
        
        # Monster stats sliders
        self.monster_health_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Health:",
            self.monster_stats["Grunt"]["health"],
            10,
            200,
            5,
            self._set_monster_health,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.monster_health_slider)
        y_pos += 30
        
        self.monster_speed_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Speed:",
            self.monster_stats["Grunt"]["speed"],
            10,
            150,
            5,
            self._set_monster_speed,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.monster_speed_slider)
        y_pos += 30
        
        self.monster_damage_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Damage:",
            self.monster_stats["Grunt"]["damage"],
            1,
            30,
            1,
            self._set_monster_damage,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.monster_damage_slider)
        y_pos += 40
        
        # Section: Monster-Specific Scaling
        self.scaling_section_y = y_pos
        section_text = "Monster-Specific Scaling"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Health scaling multiplier
        self.monster_health_scaling_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Health Scaling:",
            self.monster_scaling["Grunt"]["health_scaling"],
            1.0,
            1.5,
            0.05,
            self._set_monster_health_scaling
        )
        self.controls.append(self.monster_health_scaling_slider)
        y_pos += 30
        
        # Speed scaling multiplier
        self.monster_speed_scaling_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Speed Scaling:",
            self.monster_scaling["Grunt"]["speed_scaling"],
            0.9,
            1.2,
            0.05,
            self._set_monster_speed_scaling
        )
        self.controls.append(self.monster_speed_scaling_slider)
        y_pos += 30
        
        # Damage scaling multiplier
        self.monster_damage_scaling_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Damage Scaling:",
            self.monster_scaling["Grunt"]["damage_scaling"],
            1.0,
            1.5,
            0.05,
            self._set_monster_damage_scaling
        )
        self.controls.append(self.monster_damage_scaling_slider)
        y_pos += 40
        
        # Section: Boss Adjustments
        self.boss_section_y = y_pos
        section_text = "Boss Adjustments"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Boss type dropdown
        boss_types = list(self.boss_stats.keys())
        self.boss_type_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Boss Type:",
            boss_types,
            0,
            self._boss_type_selected
        )
        self.controls.append(self.boss_type_dropdown)
        y_pos += 30
        
        # Boss stats sliders
        self.boss_health_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Health:",
            self.boss_stats["Force"]["health"],
            100,
            1000,
            50,
            self._set_boss_health,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.boss_health_slider)
        y_pos += 30
        
        self.boss_speed_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Speed:",
            self.boss_stats["Force"]["speed"],
            10,
            100,
            5,
            self._set_boss_speed,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.boss_speed_slider)
        y_pos += 30
        
        self.boss_damage_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Damage:",
            self.boss_stats["Force"]["damage"],
            10,
            100,
            5,
            self._set_boss_damage,
            lambda x: f"{int(x)}"
        )
        self.controls.append(self.boss_damage_slider)
        y_pos += 40
        
        # Reset button
        reset_button = Button(
            (self.rect.centerx - 60, y_pos),
            (120, 30),
            "Reset to Defaults",
            self.reset
        )
        self.controls.append(reset_button)
    
    def _set_wave_difficulty_multiplier(self, value):
        """Callback for wave difficulty multiplier slider"""
        # Update global wave difficulty multiplier
        from config_extension import set_wave_difficulty_multiplier
        set_wave_difficulty_multiplier(value)
    
    def _set_monster_spawn_interval(self, value):
        """Callback for monster spawn interval slider"""
        # Update global monster spawn interval
        from config_extension import set_monster_spawn_interval
        set_monster_spawn_interval(value)
    
    def _set_base_monsters_per_wave(self, value):
        """Callback for base monsters per wave slider"""
        # Update global base monsters per wave
        from config_extension import set_wave_monster_count_base
        set_wave_monster_count_base(int(value))
    
    def _set_wave_monster_count_multiplier(self, value):
        """Callback for wave monster count multiplier slider"""
        # Update global wave monster count multiplier
        from config_extension import set_wave_monster_count_multiplier
        set_wave_monster_count_multiplier(value)
    
    def _monster_type_selected(self, index):
        """Callback for monster type dropdown"""
        monster_type = list(self.monster_stats.keys())[index]
        # Update sliders with values for selected monster type
        self.monster_health_slider.value = self.monster_stats[monster_type]["health"]
        self.monster_health_slider.update_handle()
        
        self.monster_speed_slider.value = self.monster_stats[monster_type]["speed"]
        self.monster_speed_slider.update_handle()
        
        self.monster_damage_slider.value = self.monster_stats[monster_type]["damage"]
        self.monster_damage_slider.update_handle()
        
        # Update scaling sliders
        self.monster_health_scaling_slider.value = self.monster_scaling[monster_type]["health_scaling"]
        self.monster_health_scaling_slider.update_handle()
        
        self.monster_speed_scaling_slider.value = self.monster_scaling[monster_type]["speed_scaling"]
        self.monster_speed_scaling_slider.update_handle()
        
        self.monster_damage_scaling_slider.value = self.monster_scaling[monster_type]["damage_scaling"]
        self.monster_damage_scaling_slider.update_handle()
    
    def _set_monster_health(self, value):
        """Callback for monster health slider"""
        monster_type = list(self.monster_stats.keys())[self.monster_type_dropdown.selected_index]
        # Update monster health
        self.monster_stats[monster_type]["health"] = int(value)
        # Update global monster stats
        from config_extension import update_monster_stats
        update_monster_stats(monster_type, "health", int(value))
    
    def _set_monster_speed(self, value):
        """Callback for monster speed slider"""
        monster_type = list(self.monster_stats.keys())[self.monster_type_dropdown.selected_index]
        # Update monster speed
        self.monster_stats[monster_type]["speed"] = int(value)
        # Update global monster stats
        from config_extension import update_monster_stats
        update_monster_stats(monster_type, "speed", int(value))
    
    def _set_monster_damage(self, value):
        """Callback for monster damage slider"""
        monster_type = list(self.monster_stats.keys())[self.monster_type_dropdown.selected_index]
        # Update monster damage
        self.monster_stats[monster_type]["damage"] = int(value)
        # Update global monster stats
        from config_extension import update_monster_stats
        update_monster_stats(monster_type, "damage", int(value))
    
    def _set_monster_health_scaling(self, value):
        """Callback for monster health scaling slider"""
        monster_type = list(self.monster_stats.keys())[self.monster_type_dropdown.selected_index]
        # Update monster health scaling
        self.monster_scaling[monster_type]["health_scaling"] = value
        # Store monster scaling in config module
        self._update_monster_scaling_in_config()
    
    def _set_monster_speed_scaling(self, value):
        """Callback for monster speed scaling slider"""
        monster_type = list(self.monster_stats.keys())[self.monster_type_dropdown.selected_index]
        # Update monster speed scaling
        self.monster_scaling[monster_type]["speed_scaling"] = value
        # Store monster scaling in config module
        self._update_monster_scaling_in_config()
    
    def _set_monster_damage_scaling(self, value):
        """Callback for monster damage scaling slider"""
        monster_type = list(self.monster_stats.keys())[self.monster_type_dropdown.selected_index]
        # Update monster damage scaling
        self.monster_scaling[monster_type]["damage_scaling"] = value
        # Store monster scaling in config module
        self._update_monster_scaling_in_config()
    
    def _update_monster_scaling_in_config(self):
        """Update monster scaling values in config module"""
        # Create MONSTER_SCALING in config if it doesn't exist
        module = __import__('sys').modules['config']
        if not hasattr(module, 'MONSTER_SCALING'):
            module.MONSTER_SCALING = {}
        
        # Copy monster scaling to config
        for monster_type, scaling_values in self.monster_scaling.items():
            if monster_type not in module.MONSTER_SCALING:
                module.MONSTER_SCALING[monster_type] = {}
            
            module.MONSTER_SCALING[monster_type]["health_scaling"] = scaling_values["health_scaling"]
            module.MONSTER_SCALING[monster_type]["speed_scaling"] = scaling_values["speed_scaling"]
            module.MONSTER_SCALING[monster_type]["damage_scaling"] = scaling_values["damage_scaling"]
    
    def _boss_type_selected(self, index):
        """Callback for boss type dropdown"""
        boss_type = list(self.boss_stats.keys())[index]
        # Update sliders with values for selected boss type
        self.boss_health_slider.value = self.boss_stats[boss_type]["health"]
        self.boss_health_slider.update_handle()
        
        self.boss_speed_slider.value = self.boss_stats[boss_type]["speed"]
        self.boss_speed_slider.update_handle()
        
        self.boss_damage_slider.value = self.boss_stats[boss_type]["damage"]
        self.boss_damage_slider.update_handle()
    
    def _set_boss_health(self, value):
        """Callback for boss health slider"""
        boss_type = list(self.boss_stats.keys())[self.boss_type_dropdown.selected_index]
        # Update boss health
        self.boss_stats[boss_type]["health"] = int(value)
        # Update global boss stats
        from config_extension import update_boss_stats
        update_boss_stats(boss_type, "health", int(value))
    
    def _set_boss_speed(self, value):
        """Callback for boss speed slider"""
        boss_type = list(self.boss_stats.keys())[self.boss_type_dropdown.selected_index]
        # Update boss speed
        self.boss_stats[boss_type]["speed"] = int(value)
        # Update global boss stats
        from config_extension import update_boss_stats
        update_boss_stats(boss_type, "speed", int(value))
    
    def _set_boss_damage(self, value):
        """Callback for boss damage slider"""
        boss_type = list(self.boss_stats.keys())[self.boss_type_dropdown.selected_index]
        # Update boss damage
        self.boss_stats[boss_type]["damage"] = int(value)
        # Update global boss stats
        from config_extension import update_boss_stats
        update_boss_stats(boss_type, "damage", int(value))
    
    def reset(self):
        """Reset monster and boss stats to original values"""
        # Reset monster stats
        for monster_type, stats in self.original_monster_stats.items():
            self.monster_stats[monster_type] = stats.copy()
            from config_extension import update_monster_stats_all
            update_monster_stats_all(monster_type, stats)
        
        # Reset boss stats
        for boss_type, stats in self.original_boss_stats.items():
            self.boss_stats[boss_type] = stats.copy()
            from config_extension import update_boss_stats_all
            update_boss_stats_all(boss_type, stats)
        
        # Reset monster scaling
        for monster_type in self.monster_scaling:
            self.monster_scaling[monster_type] = {
                "health_scaling": 1.2,  # Default to global scaling
                "speed_scaling": 1.0,   # By default speeds don't scale
                "damage_scaling": 1.2   # Default to global scaling
            }
        
        # Reset monster scaling in config module
        module = __import__('sys').modules['config']
        if hasattr(module, 'MONSTER_SCALING'):
            delattr(module, 'MONSTER_SCALING')
        
        # Reset global settings
        from config_extension import (
            set_wave_difficulty_multiplier,
            set_monster_spawn_interval,
            set_wave_monster_count_base,
            set_wave_monster_count_multiplier
        )
        
        set_wave_difficulty_multiplier(1.2)  # Default from config
        set_monster_spawn_interval(1.5)      # Default from config
        set_wave_monster_count_base(5)       # Default from config
        set_wave_monster_count_multiplier(1.5) # Default from config
        
        # Update sliders with default values
        for control in self.controls:
            if hasattr(control, 'reset'):
                control.reset()
        
        # Update currently selected monster/boss type sliders
        self._monster_type_selected(self.monster_type_dropdown.selected_index)
        self._boss_type_selected(self.boss_type_dropdown.selected_index)
    
    def draw(self, screen):
        """Draw the tab and its controls"""
        super().draw(screen)
        
        # Draw title
        title_text = "Monster Balance"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_rect = title_surface.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title_surface, title_rect)
        
        # Draw section headers
        y_pos = self.rect.top + 60
        
        section_text = "Global Monster Scaling"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, y_pos))
        
        y_pos = self.rect.top + 180
        
        section_text = "Monster Type Adjustments"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, y_pos))
        
        # Monster-specific scaling section
        section_text = "Monster-Specific Scaling"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, self.scaling_section_y))
        
        # Boss adjustments section
        section_text = "Boss Adjustments"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, self.boss_section_y))
