# ui/base_menu.py
"""
Base menu class for Castle Defense
"""
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:
    """Base class for all menus"""
    def __init__(self, screen):
        """
        Initialize menu
        
        Args:
            screen: Pygame surface to draw on
        """
        self.screen = screen
        self.active = False
        self.position = (WINDOW_WIDTH - 220, 100)
        self.size = (200, 300)
        self.rect = pygame.Rect(self.position, self.size)
        self.buttons = []
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.title = "Menu"
    
    def toggle(self):
        """Toggle menu visibility"""
        self.active = not self.active
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled, False otherwise
        """
        if not self.active:
            return False
        
        # Check if clicking outside menu to close it
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.rect.collidepoint(event.pos):
                self.active = False
                return True
            
            # Check button clicks
            for button in self.buttons:
                button.update(event.pos)
                if button.rect.collidepoint(event.pos):
                    button.click()
                    return True
        
        # Update button hover states
        elif event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        
        return False
    
    def draw(self):
        """Draw menu if active"""
        if not self.active:
            return
        
        # Draw menu background
        pygame.draw.rect(self.screen, (50, 50, 50), self.rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect, 2)
        
        # Draw title
        title_surface = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.top + 20))
        self.screen.blit(title_surface, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
