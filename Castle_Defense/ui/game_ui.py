# ui/game_ui.py
"""
Game UI components for Castle Defense
"""
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TOWER_TYPES, TOWER_MONSTER_COIN_COSTS
from ui.menus import Button, Slider

class GameUI:
    """Main game UI that displays resources, castle health, and wave info"""
    def __init__(self, screen):
        """
        Initialize UI with screen
        
        Args:
            screen: Pygame surface to draw on
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)
        
        # Create background surfaces for UI sections
        self.resource_bg_rect = pygame.Rect(WINDOW_WIDTH - 250, 10, 240, 200)
        
        # Play/Pause button
        self.play_pause_button = Button(
            (20, 20),
            (50, 50),
            "||",  # Pause symbol
            self.toggle_pause,
            color=(60, 60, 100),
            hover_color=(80, 80, 140)
        )
        self.is_paused = False
        
        # Game speed slider
        self.game_speed_slider = Slider(
            (20, 80),
            (150, 20),
            "Game Speed:",
            1.0,  # Default value
            0.5,  # Min value
            2.5,  # Max value
            0.5,  # Step
            self.set_game_speed,
            lambda x: f"{x:.1f}x"  # Format function
        )
    
    def toggle_pause(self):
        """Toggle the game between paused and playing states"""
        # Get the game instance from the game module
        from game import game_instance
        
        # Toggle pause state
        if self.is_paused:
            # Resume game
            self.is_paused = False
            self.play_pause_button.text = "||"  # Pause icon
            game_instance.state_manager.change_state("playing")
        else:
            # Pause game
            self.is_paused = True
            self.play_pause_button.text = "▶"  # Play icon
            game_instance.state_manager.change_state("paused")
    
    def set_game_speed(self, value):
        """
        Set the game speed
        
        Args:
            value: New game speed value
        """
        # Get the game instance from the game module
        from game import game_instance
        
        # Set the game's time scale
        game_instance.time_scale = value
    
    def handle_event(self, event):
        """
        Handle UI events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled, False otherwise
        """
        # Handle play/pause button
        if self.play_pause_button.rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.play_pause_button.click()
                return True
        
        # Handle game speed slider
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.game_speed_slider.slider_rect.collidepoint(mouse_pos) or \
               self.game_speed_slider.handle_rect.collidepoint(mouse_pos):
                # Set slider value based on click position
                slider_width = self.game_speed_slider.slider_rect.width
                slider_left = self.game_speed_slider.slider_rect.left
                slider_pos = (mouse_pos[0] - slider_left) / slider_width
                value = self.game_speed_slider.min_value + slider_pos * (self.game_speed_slider.max_value - self.game_speed_slider.min_value)
                # Round to nearest step
                value = round(value / self.game_speed_slider.step) * self.game_speed_slider.step
                # Clamp to min/max
                value = max(self.game_speed_slider.min_value, min(self.game_speed_slider.max_value, value))
                self.game_speed_slider.value = value
                self.set_game_speed(value)
                return True
        
        return False
    
    def update(self, dt):
        """
        Update UI elements
        
        Args:
            dt: Time delta in seconds
        """
        # Update button hover state
        mouse_pos = pygame.mouse.get_pos()
        if self.play_pause_button.rect.collidepoint(mouse_pos):
            self.play_pause_button.hovered = True
        else:
            self.play_pause_button.hovered = False
    
    def draw(self, resource_manager, castle, wave_manager):
        """
        Draw all UI components
        
        Args:
            resource_manager: ResourceManager with resource data
            castle: Castle instance with health data
            wave_manager: WaveManager with wave data
        """
        self.draw_resources(resource_manager)
        self.draw_castle_health(castle)
        self.draw_wave_info(wave_manager)
        
        # Draw play/pause button
        self.play_pause_button.draw(self.screen)
        
        # Draw game speed slider
        self.draw_game_speed_slider()
        
        # Draw next wave prompt if applicable and not paused
        if wave_manager.wave_completed and not self.is_paused:
            self.draw_next_wave_prompt()
    
    def draw_resources(self, resource_manager):
        """
        Draw resource display in the top right corner
        
        Args:
            resource_manager: ResourceManager with resource data
        """
        # Create semi-transparent background for resources panel
        bg_surface = pygame.Surface((self.resource_bg_rect.width, self.resource_bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((20, 20, 50, 180))  # Dark blue with transparency
        self.screen.blit(bg_surface, self.resource_bg_rect)
        
        # Draw panel border
        pygame.draw.rect(self.screen, (100, 100, 200), self.resource_bg_rect, 2)
        
        # Draw "Resources" header
        header = self.title_font.render("Resources", True, (220, 220, 255))
        header_rect = header.get_rect(midtop=(self.resource_bg_rect.centerx, self.resource_bg_rect.top + 10))
        self.screen.blit(header, header_rect)
        
        # Position for the first resource entry
        x = self.resource_bg_rect.right - 20
        y = self.resource_bg_rect.top + 40
        
        # Categorize resources
        common_resources = ["Stone", "Iron", "Copper", "Thorium", "Monster Coins"]
        special_resources = ["Force Core", "Spirit Core", "Magic Core", "Void Core"]
        item_resources = ["Unstoppable Force", "Serene Spirit"]
        
        # Display common resources first
        y = self.draw_resource_category(resource_manager, common_resources, x, y, "Materials:")
        
        # Display special resources (cores) if any exist
        has_cores = any(resource_manager.get_resource(core) > 0 for core in special_resources)
        if has_cores:
            y += 10  # Add spacing between categories
            y = self.draw_resource_category(resource_manager, special_resources, x, y, "Cores:")
        
        # Display crafted items if any exist
        has_items = any(resource_manager.get_resource(item) > 0 for item in item_resources)
        if has_items:
            y += 10  # Add spacing between categories
            y = self.draw_resource_category(resource_manager, item_resources, x, y, "Items:")
    
    def draw_resource_category(self, resource_manager, resources, x, y, category_name):
        """
        Draw a category of resources
        
        Args:
            resource_manager: ResourceManager with resource data
            resources: List of resource types to display
            x: X coordinate for right alignment
            y: Y coordinate for top alignment
            category_name: Name of the resource category
            
        Returns:
            Updated y position after drawing resources
        """
        # Draw category header
        category_text = self.small_font.render(category_name, True, (200, 200, 255))
        category_rect = category_text.get_rect(topright=(x, y))
        self.screen.blit(category_text, category_rect)
        y += 20
        
        # Draw each resource in the category
        for resource_type in resources:
            amount = resource_manager.get_resource(resource_type)
            if amount > 0 or resource_type in ["Stone", "Monster Coins"]:
                text = f"{resource_type}: {amount}"
                surface = self.font.render(text, True, (255, 255, 255))
                
                # Right-align the text
                text_rect = surface.get_rect(topright=(x, y))
                self.screen.blit(surface, text_rect)
                
                y += 25
        
        return y
    
    def draw_castle_health(self, castle):
        """
        Draw castle health display
        
        Args:
            castle: Castle instance with health data
        """
        # Draw health bar
        bar_width = 200
        bar_height = 20
        x = WINDOW_WIDTH // 2 - bar_width // 2
        y = WINDOW_HEIGHT - 30
        
        # Background
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y, bar_width, bar_height))
        
        # Health
        health_percent = castle.health / castle.max_health
        pygame.draw.rect(self.screen, (0, 200, 0), 
                         (x, y, int(bar_width * health_percent), bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 1)
        
        # Text
        text = f"Castle: {int(castle.health)}/{int(castle.max_health)}"
        surface = self.font.render(text, True, (255, 255, 255))
        text_rect = surface.get_rect(center=(WINDOW_WIDTH // 2, y - 15))
        self.screen.blit(surface, text_rect)
        
        # Additional castle stats
        stats_text = f"Damage Reduction: {int(castle.damage_reduction * 100)}%  Regen: {castle.health_regen:.1f}/s"
        stats_surface = self.small_font.render(stats_text, True, (200, 200, 200))
        stats_rect = stats_surface.get_rect(center=(WINDOW_WIDTH // 2, y - 35))
        self.screen.blit(stats_surface, stats_rect)
        
        # Add castle menu hint - now pointing to the Castle Upgrade Station
        hint_text = "Visit Castle Upgrade Station to improve defenses"
        hint_surface = self.small_font.render(hint_text, True, (255, 255, 200))
        hint_rect = hint_surface.get_rect(center=(WINDOW_WIDTH // 2, y - 55))
        self.screen.blit(hint_surface, hint_rect)
    
    def draw_wave_info(self, wave_manager):
        """
        Draw wave information in the top center
        
        Args:
            wave_manager: WaveManager with wave data
        """
        # Create wave info container
        wave_info_width = 200
        wave_info_bg = pygame.Rect(
            WINDOW_WIDTH // 2 - wave_info_width // 2, 
            10, 
            wave_info_width, 
            100 if (wave_manager.current_wave + 1) % 10 == 0 else 70
        )
        
        # Draw semi-transparent background
        bg_surface = pygame.Surface((wave_info_bg.width, wave_info_bg.height), pygame.SRCALPHA)
        bg_surface.fill((50, 20, 20, 180))  # Dark red with transparency
        self.screen.blit(bg_surface, wave_info_bg)
        
        # Draw border
        pygame.draw.rect(self.screen, (200, 100, 100), wave_info_bg, 2)
        
        # Wave number - centered at top
        text = f"Wave: {wave_manager.current_wave}"
        surface = self.title_font.render(text, True, (255, 255, 255))
        text_rect = surface.get_rect(midtop=(wave_info_bg.centerx, wave_info_bg.top + 10))
        self.screen.blit(surface, text_rect)
        
        # Monsters remaining - below wave number
        text = f"Monsters: {len(wave_manager.active_monsters)}"
        surface = self.font.render(text, True, (255, 255, 255))
        text_rect = surface.get_rect(midtop=(wave_info_bg.centerx, wave_info_bg.top + 40))
        self.screen.blit(surface, text_rect)
        
        # Next wave is boss wave indicator - below monsters
        if (wave_manager.current_wave + 1) % 10 == 0:
            text = "BOSS WAVE NEXT!"
            surface = self.font.render(text, True, (255, 100, 100))
            text_rect = surface.get_rect(midtop=(wave_info_bg.centerx, wave_info_bg.top + 70))
            self.screen.blit(surface, text_rect)
    
    def draw_game_speed_slider(self):
        """Draw the game speed slider"""
        # Draw label
        label_surface = self.font.render("Game Speed:", True, (255, 255, 255))
        self.screen.blit(label_surface, (20, 80))
        
        # Draw slider background
        slider_rect = pygame.Rect(20, 105, 150, 10)
        pygame.draw.rect(self.screen, (60, 60, 60), slider_rect)
        pygame.draw.rect(self.screen, (120, 120, 120), slider_rect, 1)
        
        # Calculate handle position
        value_range = self.game_speed_slider.max_value - self.game_speed_slider.min_value
        value_ratio = (self.game_speed_slider.value - self.game_speed_slider.min_value) / value_range
        handle_x = slider_rect.left + int(value_ratio * slider_rect.width)
        
        # Draw handle
        handle_rect = pygame.Rect(handle_x - 5, slider_rect.top - 5, 10, 20)
        pygame.draw.rect(self.screen, (150, 150, 200), handle_rect)
        
        # Draw value
        value_text = f"{self.game_speed_slider.value:.1f}x"
        value_surface = self.font.render(value_text, True, (255, 255, 255))
        self.screen.blit(value_surface, (175, 100))
        
        # Store handle rect for interactions
        self.game_speed_slider.slider_rect = slider_rect
        self.game_speed_slider.handle_rect = handle_rect
    
    def draw_next_wave_prompt(self):
        """Draw prompt to start next wave"""
        # Create a pulsing effect for the prompt
        pulse = (pygame.time.get_ticks() % 2000) / 2000  # 0 to 1 over 2 seconds
        pulse_value = 0.7 + 0.3 * abs(pulse - 0.5) * 2  # 0.7 to 1.0 pulsing
        
        text_color = (int(255 * pulse_value), int(255 * pulse_value), 0)
        
        text = "Press SPACE to start next wave"
        surface = self.font.render(text, True, text_color)
        text_rect = surface.get_rect(center=(WINDOW_WIDTH // 2, 150))
        
        # Add a background to make text more visible
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(bg_surface, bg_rect)
        
        # Draw text
        self.screen.blit(surface, text_rect)


class TowerPlacementUI:
    """UI for selecting and placing towers"""
    def __init__(self, screen, game):
        """
        Initialize tower placement UI
        
        Args:
            screen: Pygame surface to draw on
            game: Game instance for callbacks
        """
        self.screen = screen
        self.game = game
        self.font = pygame.font.Font(None, 20)
        
        # Create buttons for each tower type
        self.buttons = []
        tower_types = list(TOWER_TYPES.keys())
        
        for i, tower_type in enumerate(tower_types):
            button_x = 10 + i * 110
            button_y = WINDOW_HEIGHT - 70
            
            self.buttons.append(Button(
                (button_x, button_y),
                (100, 60),
                tower_type,
                lambda t=tower_type: self.select_tower(t)
            ))
    
    def select_tower(self, tower_type):
        """
        Callback when tower type is selected
        
        Args:
            tower_type: Type of tower to place
        """
        self.game.enter_tower_placement_mode(tower_type)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            for button in self.buttons:
                button.update(mouse_pos)
                if button.rect.collidepoint(mouse_pos):
                    button.click()
                    return True
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update(mouse_pos)
        
        return False
    
    def draw(self, resource_manager):
        """
        Draw tower selection buttons
        
        Args:
            resource_manager: ResourceManager to check if player has enough resources
        """
        # Draw tower selection buttons
        for button in self.buttons:
            button.draw(self.screen)
            
            # Get tower type from button text
            tower_type = button.text
            
            # Get costs
            tower_cost = TOWER_TYPES.get(tower_type, {}).get("cost", {})
            monster_coin_cost = TOWER_MONSTER_COIN_COSTS.get(tower_type, 0)
            
            # Draw cost under button
            cost_text = ", ".join(f"{amt} {res}" for res, amt in tower_cost.items())
            
            # Add Monster Coin cost
            if monster_coin_cost > 0:
                cost_text += f", {monster_coin_cost} Monster Coins"
                
            cost_surface = self.font.render(cost_text, True, (200, 200, 200))
            cost_rect = cost_surface.get_rect(center=(button.rect.centerx, button.rect.bottom + 15))
            self.screen.blit(cost_surface, cost_rect)
            
            # Indicate if player has enough resources
            has_resources = resource_manager.has_resources_for_tower(tower_cost, monster_coin_cost)
            color = (0, 255, 0) if has_resources else (255, 0, 0)
            pygame.draw.rect(self.screen, color, button.rect, 2)
