# ui/dev_menu/main_menu.py
"""
Main developer menu class for Castle Defense game
"""
import pygame
from .components import TabButton
from .monster_tab import MonsterBalanceTab
from .economy_tab import EconomyTab
from .tower_tab import TowerUpgradeTab
from .config_tab import ConfigurationTab
from .buildings_tab import BuildingsTab

class DeveloperMenu:
    """Developer menu for game balance and testing"""
    def __init__(self, screen, game_instance):
        """
        Initialize developer menu
        
        Args:
            screen: Pygame surface to draw on
            game_instance: Game instance for callbacks
        """
        self.screen = screen
        self.game = game_instance
        self.visible = False
        
        # Calculate menu dimensions
        menu_width = int(screen.get_width() * 0.8)
        menu_height = int(screen.get_height() * 0.8)
        self.rect = pygame.Rect(
            (screen.get_width() - menu_width) // 2,
            (screen.get_height() - menu_height) // 2,
            menu_width,
            menu_height
        )
        
        # Setup tabs
        self.current_tab = 0
        self.tab_buttons = []
        self.tabs = []
        self._init_tabs()
    
    def _init_tabs(self):
        """Initialize tab buttons and tab content"""
        # Define tab area (below tab buttons)
        tab_button_height = 40
        tab_area = pygame.Rect(
            self.rect.left,
            self.rect.top + tab_button_height,
            self.rect.width,
            self.rect.height - tab_button_height
        )
        
        # Create tab instances
        self.tabs = [
            MonsterBalanceTab(tab_area, self.game),
            EconomyTab(tab_area, self.game),
            TowerUpgradeTab(tab_area, self.game),
            BuildingsTab(tab_area, self.game),
            ConfigurationTab(tab_area, self.game)
        ]
        
        # Create tab buttons
        tab_names = ["Monsters", "Economy", "Towers", "Buildings", "Config"]
        tab_width = self.rect.width // len(tab_names)
        
        for i, name in enumerate(tab_names):
            button = TabButton(
                (self.rect.left + i * tab_width, self.rect.top),
                tab_width,
                name,
                i
            )
            if i == self.current_tab:
                button.active = True
            self.tab_buttons.append(button)
    
    def toggle(self):
        """Toggle menu visibility"""
        self.visible = not self.visible
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        if not self.visible:
            return
        
        # Check for tab button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.tab_buttons:
                if button.rect.collidepoint(mouse_pos):
                    self._set_active_tab(button.tab_id)
                    return
        
        # Pass event to current tab
        self.tabs[self.current_tab].handle_event(event)
    
    def _set_active_tab(self, tab_id):
        """Set active tab"""
        if 0 <= tab_id < len(self.tabs):
            self.current_tab = tab_id
            
            # Update button states
            for button in self.tab_buttons:
                button.active = (button.tab_id == tab_id)
    
    def update(self, dt):
        """Update menu state"""
        if not self.visible:
            return
        
        # Get current mouse position for updating hover states
        mouse_pos = pygame.mouse.get_pos()
        
        # Update tab button hover states
        for button in self.tab_buttons:
            button.update(mouse_pos)
        
        # Update active tab
        self.tabs[self.current_tab].update(dt)
    
    def draw(self):
        """Draw menu on screen"""
        if not self.visible:
            return
        
        # Draw menu background
        pygame.draw.rect(self.screen, (30, 30, 30), self.rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.rect, 2)
        
        # Draw tab buttons
        for button in self.tab_buttons:
            button.draw(self.screen)
        
        # Draw active tab
        self.tabs[self.current_tab].draw(self.screen)
