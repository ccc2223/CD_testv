# states/tower_placement_state.py
"""
Tower placement state for Castle Defense
"""
import pygame
import math
from .game_state import GameState
from features.towers.factory import TowerFactory
from config import TOWER_MONSTER_COIN_COSTS

class TowerPlacementState(GameState):
    """
    State for placing towers on the game map
    """
    def __init__(self, game):
        """
        Initialize tower placement state
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        self.tower_type = None
        self.tower_preview = None
    
    def enter(self):
        """
        Called when entering tower placement state
        """
        # This will be set by the method that triggers state change
        self.tower_type = None
        self.tower_preview = None
    
    def exit(self):
        """
        Called when exiting tower placement state
        """
        self.tower_type = None
        self.tower_preview = None
    
    def set_tower_type(self, tower_type):
        """
        Set the type of tower to place
        
        Args:
            tower_type: String tower type (e.g., "Archer", "Sniper")
        """
        self.tower_type = tower_type
        
        # Create appropriate tower preview using the factory
        if tower_type:
            try:
                self.tower_preview = TowerFactory.create_tower(tower_type, (0, 0))
            except ValueError:
                self.tower_preview = None
    
    def handle_events(self, events):
        """
        Handle events during tower placement
        
        Args:
            events: List of pygame events
            
        Returns:
            Boolean indicating if events were handled
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.tower_preview:
            self.tower_preview.position = mouse_pos
            self.tower_preview.rect.center = mouse_pos
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Attempt to place tower
                    if self.place_tower(mouse_pos):
                        self.game.state_manager.change_state("playing")
                        return True
                elif event.button == 3:  # Right click
                    # Cancel tower placement
                    self.game.state_manager.change_state("playing")
                    return True
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Cancel tower placement on Escape
                    self.game.state_manager.change_state("playing")
                    return True
        
        return False
    
    def update(self, dt):
        """
        Update tower placement logic
        
        Args:
            dt: Time delta in seconds
        """
        # Most of the logic is in handle_events and draw
        pass
    
    def draw(self, screen):
        """
        Draw the game with tower placement overlay
        
        Args:
            screen: Pygame surface to draw on
        """
        # First draw the base game
        self.game.states["playing"].draw(screen)
        
        # Then draw the tower preview
        if self.tower_preview:
            mouse_pos = pygame.mouse.get_pos()
            self.tower_preview.position = mouse_pos
            self.tower_preview.rect.center = mouse_pos
            
            # Draw with transparency based on valid position and resources
            is_valid = self.is_valid_tower_position(mouse_pos)
            
            # Get tower costs
            tower_cost = self.game.TOWER_TYPES.get(self.tower_type, {}).get("cost", {})
            monster_coin_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 0)
            
            # Check if we have all required resources
            has_resources = self.game.resource_manager.has_resources_for_tower(
                tower_cost, monster_coin_cost
            )
            
            # Create transparent surface
            alpha_surface = pygame.Surface(self.tower_preview.rect.size, pygame.SRCALPHA)
            
            if is_valid and has_resources:
                # Valid position - use tower color with transparency
                color = list(self.tower_preview.color) + [128]  # 50% transparency
            else:
                # Invalid position - use red with transparency
                color = [255, 0, 0, 128]  # Red with 50% transparency
            
            # Draw the tower preview on the transparent surface
            pygame.draw.rect(alpha_surface, color, 
                            (0, 0, self.tower_preview.rect.width, self.tower_preview.rect.height))
            
            # Blit the transparent surface to the screen
            screen.blit(alpha_surface, self.tower_preview.rect.topleft)
            
            # Draw range indicator using scaled range
            line_width = max(1, self.game.scale_value(1))
            if is_valid and has_resources:
                # Draw pulsing range indicator when valid
                pulse_factor = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.1 + 0.9
                pulse_range = int(self.tower_preview.range * pulse_factor)
                pygame.draw.circle(screen, (200, 255, 200), 
                                mouse_pos, 
                                pulse_range, line_width)
            else:
                # Draw normal range indicator when invalid
                pygame.draw.circle(screen, (255, 100, 100), 
                                mouse_pos, 
                                int(self.tower_preview.range), line_width)
    
    def is_valid_tower_position(self, position):
        """
        Check if position is valid for tower placement
        
        Args:
            position: Tuple of (x, y) coordinates
            
        Returns:
            True if position is valid, False otherwise
        """
        return self.game.is_valid_tower_position(position)
    
    def place_tower(self, position):
        """
        Attempt to place a tower at the specified position
        
        Args:
            position: Tuple of (x, y) coordinates
            
        Returns:
            True if tower was placed, False otherwise
        """
        if not self.tower_type:
            return False
        
        # Check if position is valid
        if not self.is_valid_tower_position(position):
            return False
        
        # Get tower costs
        tower_cost = self.game.TOWER_TYPES.get(self.tower_type, {}).get("cost", {})
        monster_coin_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 0)
        
        # Check if player has enough resources and spend them
        if not self.game.resource_manager.spend_resources_for_tower(tower_cost, monster_coin_cost):
            return False
        
        # Create and place the tower using the factory
        tower = TowerFactory.create_tower(self.tower_type, position)
        self.game.towers.append(tower)
        
        return True
