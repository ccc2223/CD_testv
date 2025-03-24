# states/main_menu_state.py
"""
Main menu state for Castle Defense
"""
import pygame
from .game_state import GameState
from ui.main_menu import MainMenu

class MainMenuState(GameState):
    """
    Main menu state - displays the game's main menu
    """
    def __init__(self, game):
        """
        Initialize main menu state
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        self.menu = MainMenu(game.screen, game)
    
    def enter(self):
        """Called when entering main menu state"""
        # Reset menu animation if needed
        if hasattr(self.menu, 'time'):
            self.menu.time = 0
            self.menu.title_animation_complete = False
            
            # Reset title blocks to starting positions
            for block in self.menu.title_blocks:
                block['current_pos'] = block['start_pos']
                block['landed'] = False
    
    def handle_events(self, events):
        """
        Handle events during main menu state
        
        Args:
            events: List of pygame events
            
        Returns:
            Boolean indicating if events were handled
        """
        for event in events:
            # Let the menu handle events first
            if self.menu.handle_event(event):
                return True
            
            # Check for escape key to exit game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False
                return True
        
        return False
    
    def update(self, dt):
        """
        Update main menu logic
        
        Args:
            dt: Time delta in seconds
        """
        self.menu.update(dt)
    
    def draw(self, screen):
        """
        Draw main menu
        
        Args:
            screen: Pygame surface to draw on
        """
        self.menu.draw()
