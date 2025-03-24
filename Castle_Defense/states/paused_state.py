# states/paused_state.py
"""
Paused state for Castle Defense
"""
import pygame
from .game_state import GameState

class PausedState(GameState):
    """
    Paused game state - game is frozen but user can resume
    """
    def __init__(self, game):
        """
        Initialize paused state
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        self.overlay_alpha = 180  # Semi-transparent overlay
        self.menu_options = [
            {
                "text": "Resume Game",
                "action": self.resume_game
            },
            {
                "text": "Save Game",
                "action": self.save_game
            },
            {
                "text": "Exit to Menu", 
                "action": None  # Placeholder for future menu state
            }
        ]
        self.selected_option = 0
    
    def enter(self):
        """Called when entering paused state"""
        # Update the game UI play/pause button state
        self.game.game_ui.is_paused = True
        self.game.game_ui.play_pause_button.text = "▶"  # Play icon
        
        # Set paused flag in playing state
        if hasattr(self.game.states["playing"], "paused"):
            self.game.states["playing"].paused = True
    
    def exit(self):
        """Called when exiting paused state"""
        # Update the game UI play/pause button state
        self.game.game_ui.is_paused = False
        self.game.game_ui.play_pause_button.text = "||"  # Pause icon
        
        # Clear paused flag in playing state
        if hasattr(self.game.states["playing"], "paused"):
            self.game.states["playing"].paused = False
    
    def handle_events(self, events):
        """
        Handle events during paused state
        
        Args:
            events: List of pygame events
            
        Returns:
            Boolean indicating if events were handled
        """
        # First check if play/pause button was clicked
        for event in events:
            if self.game.game_ui.handle_event(event):
                return True
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Resume game on Escape
                    self.resume_game()
                    return True
                
                elif event.key == pygame.K_UP:
                    # Move selection up
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    return True
                
                elif event.key == pygame.K_DOWN:
                    # Move selection down
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    return True
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Activate selected option
                    option = self.menu_options[self.selected_option]
                    if option["action"]:
                        option["action"]()
                    return True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicking on menu options
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.menu_options):
                        option_rect = self.get_option_rect(i)
                        if option_rect.collidepoint(mouse_pos) and option["action"]:
                            option["action"]()
                            return True
        
        return False
    
    def update(self, dt):
        """
        Update paused state logic
        
        Args:
            dt: Time delta in seconds
        """
        # Update game UI for button hovering
        self.game.game_ui.update(dt)
    
    def draw(self, screen):
        """
        Draw paused state
        
        Args:
            screen: Pygame surface to draw on
        """
        # First draw the base game (frozen)
        self.game.states["playing"].draw(screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.game.WINDOW_WIDTH, self.game.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.overlay_alpha))
        screen.blit(overlay, (0, 0))
        
        # Draw the play/pause button
        self.game.game_ui.play_pause_button.draw(screen)
        
        # Draw the game speed slider
        self.game.game_ui.draw_game_speed_slider()
        
        # Draw pause menu
        self.draw_pause_menu(screen)
    
    def draw_pause_menu(self, screen):
        """
        Draw the pause menu
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw background panel
        panel_width = self.game.scale_value(300)
        panel_height = self.game.scale_value(250)
        panel_rect = pygame.Rect(
            (self.game.WINDOW_WIDTH - panel_width) // 2,
            (self.game.WINDOW_HEIGHT - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Draw panel with border
        pygame.draw.rect(screen, (40, 40, 60), panel_rect)
        pygame.draw.rect(screen, (100, 100, 150), panel_rect, self.game.scale_value(2))
        
        # Draw "PAUSED" text
        font_size = self.game.scale_value(36)
        font = pygame.font.Font(None, font_size)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(midtop=(panel_rect.centerx, panel_rect.top + self.game.scale_value(20)))
        screen.blit(text, text_rect)
        
        # Draw menu options
        option_font_size = self.game.scale_value(24)
        option_font = pygame.font.Font(None, option_font_size)
        option_spacing = self.game.scale_value(40)
        
        for i, option in enumerate(self.menu_options):
            # Determine if this option is selected
            is_selected = (i == self.selected_option)
            
            # Set text color - brighter for selected option
            text_color = (255, 255, 100) if is_selected else (200, 200, 200)
            
            # Create text surface
            text = option_font.render(option["text"], True, text_color)
            
            # Position and draw text
            y_pos = panel_rect.top + self.game.scale_value(80) + i * option_spacing
            text_rect = text.get_rect(center=(panel_rect.centerx, y_pos))
            screen.blit(text, text_rect)
            
            # Draw selection indicator if this option is selected
            if is_selected:
                indicator_rect = text_rect.inflate(self.game.scale_value(20), self.game.scale_value(10))
                pygame.draw.rect(screen, (100, 100, 180), indicator_rect, self.game.scale_value(2))
    
    def get_option_rect(self, index):
        """
        Get the rect for a menu option
        
        Args:
            index: Index of the option
            
        Returns:
            Pygame Rect for the option
        """
        panel_width = self.game.scale_value(300)
        panel_rect_x = (self.game.WINDOW_WIDTH - panel_width) // 2
        panel_rect_y = (self.game.WINDOW_HEIGHT - self.game.scale_value(250)) // 2
        
        option_height = self.game.scale_value(30)
        option_width = self.game.scale_value(200)
        option_y = panel_rect_y + self.game.scale_value(80) + index * self.game.scale_value(40)
        
        return pygame.Rect(
            (self.game.WINDOW_WIDTH - option_width) // 2,
            option_y - option_height // 2,
            option_width,
            option_height
        )
    
    def resume_game(self):
        """Resume the game by changing back to playing state"""
        self.game.state_manager.change_state("playing")
    
    def save_game(self):
        """Save the game"""
        self.game.save_manager.save_game()
        # Optional: Show a "game saved" message
