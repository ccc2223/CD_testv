# states/game_over_state.py
"""
Game over state for Castle Defense
"""
import pygame
import math
from .game_state import GameState

class GameOverState(GameState):
    """
    Game over state - displayed when the player loses, but allows continuing
    """
    def __init__(self, game):
        """
        Initialize game over state
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        self.time_in_state = 0
        self.auto_continue_time = 15.0  # Auto-continue after 15 seconds
        self.setback_wave = 1  # Default setback
        self.current_wave = 0  # Will be set when entering the state
    
    def enter(self):
        """Called when entering game over state"""
        self.time_in_state = 0
        self.current_wave = self.game.wave_manager.current_wave
        
        # Calculate setback wave based on current progress
        if self.current_wave >= 11:
            # If player has reached wave 11+, setback 10 waves
            self.setback_wave = max(1, self.current_wave - 10)
        else:
            # Otherwise, reset to wave 1
            self.setback_wave = 1
    
    def handle_events(self, events):
        """
        Handle events during game over state
        
        Args:
            events: List of pygame events
            
        Returns:
            Boolean indicating if events were handled
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Exit game on Escape
                    self.game.running = False
                    return True
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    # Continue immediately on Enter/Space
                    self.continue_game()
                    return True
        
        return False
    
    def update(self, dt):
        """
        Update game over logic
        
        Args:
            dt: Time delta in seconds
        """
        self.time_in_state += dt
        
        # Auto-continue after the timer expires
        if self.time_in_state >= self.auto_continue_time:
            self.continue_game()
    
    def continue_game(self):
        """Reset castle health and continue the game from setback wave"""
        # Reset castle health to full
        self.game.castle.health = self.game.castle.max_health
        
        # Set the wave number to the setback wave
        self.game.wave_manager.current_wave = self.setback_wave - 1  # -1 because starting next wave increments
        
        # Clear any active monsters and reset wave state
        self.game.wave_manager.active_monsters = []
        self.game.wave_manager.wave_active = False
        self.game.wave_manager.wave_completed = True
        self.game.wave_manager.monsters_to_spawn = 0
        
        # Change back to playing state
        self.game.state_manager.change_state("playing")
    
    def draw(self, screen):
        """
        Draw game over screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # First draw the base game (frozen)
        self.game.states["playing"].draw(screen)
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.game.WINDOW_WIDTH, self.game.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
        screen.blit(overlay, (0, 0))
        
        # Draw castle destroyed text with pulsing effect
        pulse = (math.sin(pygame.time.get_ticks() * 0.003) + 1) * 0.2 + 0.8
        font_size = int(self.game.scale_value(60) * pulse)
        font = pygame.font.Font(None, font_size)
        text = font.render("Castle Destroyed!", True, (255, 80, 80))
        text_rect = text.get_rect(center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT // 2 - 30))
        screen.blit(text, text_rect)
        
        # Draw rebuilding message
        small_font_size = self.game.scale_value(36)
        font = pygame.font.Font(None, small_font_size)
        rebuild_text = "Rebuilding..."
        text = font.render(rebuild_text, True, (200, 200, 255))
        text_rect = text.get_rect(center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT // 2 + 30))
        screen.blit(text, text_rect)
        
        # Draw wave setback info
        info_font_size = self.game.scale_value(28)
        font = pygame.font.Font(None, info_font_size)
        if self.current_wave >= 11:
            setback_text = f"Setting back 10 waves (Wave {self.current_wave} → {self.setback_wave})"
        else:
            setback_text = f"Restarting from Wave {self.setback_wave}"
        
        text = font.render(setback_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT // 2 + 80))
        screen.blit(text, text_rect)
        
        # Draw countdown
        remaining_time = max(0, self.auto_continue_time - self.time_in_state)
        countdown_text = f"Continuing in {remaining_time:.1f} seconds..."
        countdown_surface = font.render(countdown_text, True, (200, 200, 200))
        countdown_rect = countdown_surface.get_rect(center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT // 2 + 120))
        screen.blit(countdown_surface, countdown_rect)
        
        # Draw "Press any key to continue" message
        prompt_font_size = self.game.scale_value(24)
        font = pygame.font.Font(None, prompt_font_size)
        text = font.render("Press ENTER to continue immediately", True, (200, 200, 200))
        text_rect = text.get_rect(center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT // 2 + 170))
        screen.blit(text, text_rect)
        
        # Draw ESC to quit
        text = font.render("Press ESC to quit", True, (200, 200, 200))
        text_rect = text.get_rect(center=(self.game.WINDOW_WIDTH // 2, self.game.WINDOW_HEIGHT // 2 + 200))
        screen.blit(text, text_rect)
