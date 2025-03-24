# ui/dev_menu/config_tab.py
"""
Configuration tab for developer menu
"""
import pygame
import json
import os
import math
from .components import Tab, Slider, Button, TextInput, Checkbox, DropdownMenu

# File path for saving configurations
CONFIG_DIR = "configs"
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

class ConfigurationTab(Tab):
    """Tab for saving, loading, and handling game configurations"""
    def __init__(self, rect, game_instance):
        """
        Initialize configuration tab
        
        Args:
            rect: Pygame Rect defining the tab area
            game_instance: Reference to the Game instance
        """
        super().__init__(rect)
        self.game = game_instance
        
        # Configuration file handling
        self.config_files = self._get_config_files()
        self.selected_config = None
        self.new_config_name = "new_config"
        
        # Game settings
        self.continuous_wave = False
        self.game_speed = 1.0
        self.god_mode = False
        
        # Initialize controls
        self._init_controls()
    
    def _get_config_files(self):
        """Get list of available configuration files"""
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        
        # Get list of json files in config directory
        config_files = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
        return config_files
    
    def _init_controls(self):
        """Initialize all controls for this tab"""
        y_pos = self.rect.top + 20
        width = self.rect.width - 40
        
        # Title
        title_text = "Game Settings & Configurations"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_pos = (self.rect.left + 20, y_pos)
        y_pos += 30
        
        # Section: Game Settings
        section_text = "Game Settings"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # Continuous wave mode checkbox
        self.continuous_wave_checkbox = Checkbox(
            (self.rect.left + 20, y_pos),
            "Continuous Wave Mode",
            self.continuous_wave,
            self._set_continuous_wave
        )
        self.controls.append(self.continuous_wave_checkbox)
        y_pos += 30
        
        # God mode checkbox
        self.god_mode_checkbox = Checkbox(
            (self.rect.left + 20, y_pos),
            "God Mode (Castle Invulnerable)",
            self.god_mode,
            self._set_god_mode
        )
        self.controls.append(self.god_mode_checkbox)
        y_pos += 30
        
        # Game speed slider
        self.game_speed_slider = Slider(
            (self.rect.left + 20, y_pos),
            width,
            "Game Speed:",
            self.game_speed,
            0.5,
            3.0,
            0.5,
            self._set_game_speed,
            lambda x: f"{x:.1f}x"
        )
        self.controls.append(self.game_speed_slider)
        y_pos += 30
        
        # Wave jump buttons
        y_pos += 10
        jump_wave_label = self.font.render("Jump to Wave:", True, (255, 255, 255))
        
        # Add buttons for wave jumps
        btn_width = 60
        btn_height = 30
        btn_spacing = 10
        total_width = 4 * btn_width + 3 * btn_spacing
        start_x = self.rect.left + (self.rect.width - total_width) // 2
        
        self.controls.append(Button(
            (start_x, y_pos),
            (btn_width, btn_height),
            "5",
            lambda: self._jump_to_wave(5)
        ))
        
        self.controls.append(Button(
            (start_x + btn_width + btn_spacing, y_pos),
            (btn_width, btn_height),
            "10",
            lambda: self._jump_to_wave(10)
        ))
        
        self.controls.append(Button(
            (start_x + 2 * (btn_width + btn_spacing), y_pos),
            (btn_width, btn_height),
            "20",
            lambda: self._jump_to_wave(20)
        ))
        
        self.controls.append(Button(
            (start_x + 3 * (btn_width + btn_spacing), y_pos),
            (btn_width, btn_height),
            "50",
            lambda: self._jump_to_wave(50)
        ))
        y_pos += 40
        
        # Resource edit buttons
        resource_label = self.font.render("Edit Resources:", True, (255, 255, 255))
        
        # Add resources +100/+500 buttons for Stone, Iron, Monster Coins
        btn_width = 90
        btn_height = 25
        btn_spacing = 10
        
        # Stone resources
        self.controls.append(Button(
            (self.rect.left + 20, y_pos),
            (btn_width, btn_height),
            "+100 Stone",
            lambda: self._add_resource("Stone", 100)
        ))
        
        self.controls.append(Button(
            (self.rect.left + 20 + btn_width + btn_spacing, y_pos),
            (btn_width, btn_height),
            "+500 Stone",
            lambda: self._add_resource("Stone", 500)
        ))
        y_pos += btn_height + 5
        
        # Iron resources
        self.controls.append(Button(
            (self.rect.left + 20, y_pos),
            (btn_width, btn_height),
            "+100 Iron",
            lambda: self._add_resource("Iron", 100)
        ))
        
        self.controls.append(Button(
            (self.rect.left + 20 + btn_width + btn_spacing, y_pos),
            (btn_width, btn_height),
            "+500 Iron",
            lambda: self._add_resource("Iron", 500)
        ))
        y_pos += btn_height + 5
        
        # Monster Coins resources
        self.controls.append(Button(
            (self.rect.left + 20, y_pos),
            (btn_width, btn_height),
            "+10 MCoins",
            lambda: self._add_resource("Monster Coins", 10)
        ))
        
        self.controls.append(Button(
            (self.rect.left + 20 + btn_width + btn_spacing, y_pos),
            (btn_width, btn_height),
            "+50 MCoins",
            lambda: self._add_resource("Monster Coins", 50)
        ))
        y_pos += 50
        
        # Section: Configuration Files
        section_text = "Configuration Files"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        section_pos = (self.rect.left + 20, y_pos)
        y_pos += 25
        
        # New config name input
        self.config_name_input = TextInput(
            (self.rect.left + 20, y_pos),
            width,
            "New Config Name:",
            "new_config"
        )
        self.controls.append(self.config_name_input)
        y_pos += 30
        
        # Save config button
        self.save_config_button = Button(
            (self.rect.left + 20, y_pos),
            (width // 2 - 10, 30),
            "Save Configuration",
            self._save_configuration
        )
        self.controls.append(self.save_config_button)
        
        # Load config button
        self.load_config_button = Button(
            (self.rect.left + width // 2 + 10, y_pos),
            (width // 2 - 10, 30),
            "Load Configuration",
            self._load_configuration
        )
        self.controls.append(self.load_config_button)
        y_pos += 40
        
        # Config files dropdown
        self.config_dropdown = DropdownMenu(
            (self.rect.left + 20, y_pos),
            width,
            "Available Configs:",
            self.config_files if self.config_files else ["No configs available"],
            0,
            self._config_selected
        )
        self.controls.append(self.config_dropdown)
        y_pos += 40
        
        # Reset all button
        reset_button = Button(
            (self.rect.centerx - 60, y_pos),
            (120, 30),
            "Reset All to Defaults",
            self._reset_all
        )
        self.controls.append(reset_button)
    
    def _set_continuous_wave(self, value):
        """Callback for continuous wave checkbox"""
        self.continuous_wave = value
        # Update game's continuous wave mode
        if self.game:
            self.game.wave_manager.continuous_wave = value
    
    def _set_god_mode(self, value):
        """Callback for god mode checkbox"""
        self.god_mode = value
        # Apply god mode to castle
        if self.game and self.game.castle:
            if value:
                # Store original castle take_damage method
                if not hasattr(self.game.castle, '_original_take_damage'):
                    self.game.castle._original_take_damage = self.game.castle.take_damage
                
                # Replace with invulnerable version
                self.game.castle.take_damage = lambda damage: True
            else:
                # Restore original take_damage method if it exists
                if hasattr(self.game.castle, '_original_take_damage'):
                    self.game.castle.take_damage = self.game.castle._original_take_damage
    
    def _set_game_speed(self, value):
        """Callback for game speed slider"""
        self.game_speed = value
        # Update game's time scale
        if self.game:
            self.game.time_scale = value
    
    def _jump_to_wave(self, wave):
        """Jump to specified wave number"""
        if self.game:
            # Set wave manager wave number
            self.game.wave_manager.current_wave = wave - 1  # Subtract 1 because starting next wave will increment
            # Complete current wave if one is active
            self.game.wave_manager.wave_active = False
            self.game.wave_manager.wave_completed = True
            # Clear any active monsters
            self.game.wave_manager.active_monsters = []
            self.game.wave_manager.monsters_to_spawn = 0
            # Ready for next wave
            self.game.wave_manager.start_next_wave()
    
    def _add_resource(self, resource_type, amount):
        """Add resources to player inventory"""
        if self.game and self.game.resource_manager:
            self.game.resource_manager.add_resource(resource_type, amount)
    
    def _save_configuration(self):
        """Save current game configuration to file"""
        # Get config name from text input
        config_name = self.config_name_input.text.strip()
        if not config_name:
            config_name = "config"
        
        # Ensure file has .json extension
        if not config_name.endswith('.json'):
            config_name += '.json'
        
        # Collect all configuration data
        from config_extension import get_all_config_values
        config_data = get_all_config_values()
        
        # Save to file
        filepath = os.path.join(CONFIG_DIR, config_name)
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        # Update config files list
        self.config_files = self._get_config_files()
        
        # Update dropdown
        self.config_dropdown.options = self.config_files if self.config_files else ["No configs available"]
        
        # Select the newly saved config
        if config_name in self.config_files:
            self.config_dropdown.selected_index = self.config_files.index(config_name)
            self.selected_config = config_name
    
    def _load_configuration(self):
        """Load selected configuration from file"""
        if not self.selected_config or self.selected_config == "No configs available":
            return
        
        # Load from file
        filepath = os.path.join(CONFIG_DIR, self.selected_config)
        try:
            with open(filepath, 'r') as f:
                config_data = json.load(f)
            
            # Apply configuration to game
            from config_extension import apply_all_config_values
            apply_all_config_values(config_data)
            
            # Update UI controls with new values
            for tab in self.game.dev_menu.tabs:
                # Reset controls with new values
                # This is a bit of a hack, but it should work
                for control in tab.controls:
                    if hasattr(control, 'reset'):
                        control.reset()
                
                # Special handling for dropdowns to update their selections
                if hasattr(tab, '_monster_type_selected') and hasattr(tab, 'monster_type_dropdown'):
                    tab._monster_type_selected(tab.monster_type_dropdown.selected_index)
                if hasattr(tab, '_boss_type_selected') and hasattr(tab, 'boss_type_dropdown'):
                    tab._boss_type_selected(tab.boss_type_dropdown.selected_index)
                if hasattr(tab, '_tower_type_selected') and hasattr(tab, 'tower_dropdown'):
                    tab._tower_type_selected(tab.tower_dropdown.selected_index)
                if hasattr(tab, '_item_selected') and hasattr(tab, 'item_dropdown'):
                    tab._item_selected(tab.item_dropdown.selected_index)
                    
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration: {e}")
    
    def _config_selected(self, index):
        """Callback for config dropdown"""
        if index < len(self.config_files):
            self.selected_config = self.config_files[index]
    
    def _reset_all(self):
        """Reset all game settings to defaults"""
        # Call reset method on all tabs
        for tab in self.game.dev_menu.tabs:
            if hasattr(tab, 'reset'):
                tab.reset()
        
        # Reset game settings
        self.continuous_wave = False
        self.game_speed = 1.0
        self.god_mode = False
        
        if self.game:
            self.game.wave_manager.continuous_wave = False
            self.game.time_scale = 1.0
            
            # Reset god mode if active
            if hasattr(self.game.castle, '_original_take_damage'):
                self.game.castle.take_damage = self.game.castle._original_take_damage
        
        # Update UI controls
        self.continuous_wave_checkbox.checked = False
        self.god_mode_checkbox.checked = False
        self.game_speed_slider.value = 1.0
        self.game_speed_slider.update_handle()
    
    def update(self, dt):
        """Update controls that need updating"""
        super().update(dt)
        
        # Refresh config files list periodically
        self.config_files = self._get_config_files()
        if not self.config_files:
            self.config_dropdown.options = ["No configs available"]
        elif self.config_dropdown.options != self.config_files:
            selected_index = min(self.config_dropdown.selected_index, len(self.config_files) - 1)
            self.config_dropdown.options = self.config_files
            self.config_dropdown.selected_index = selected_index
            if selected_index >= 0 and selected_index < len(self.config_files):
                self.selected_config = self.config_files[selected_index]
    
    def draw(self, screen):
        """Draw the tab and its controls"""
        super().draw(screen)
        
        # Draw title
        title_text = "Game Settings & Configurations"
        title_surface = self.title_font.render(title_text, True, (255, 255, 200))
        title_rect = title_surface.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title_surface, title_rect)
        
        # Draw section headers
        y_pos = self.rect.top + 60
        
        section_text = "Game Settings"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, y_pos))
        
        y_pos = self.rect.top + 160
        
        screen.blit(self.font.render("Jump to Wave:", True, (255, 255, 255)), 
                   (self.rect.left + 20, y_pos))
        
        y_pos = self.rect.top + 210
        
        screen.blit(self.font.render("Edit Resources:", True, (255, 255, 255)), 
                   (self.rect.left + 20, y_pos))
        
        y_pos = self.rect.top + 300
        
        section_text = "Configuration Files"
        section_surface = self.font.render(section_text, True, (200, 200, 255))
        screen.blit(section_surface, (self.rect.left + 20, y_pos))
