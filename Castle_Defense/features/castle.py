# features/castle.py
"""
Castle implementation for the Castle Defense game
"""
import pygame
from config import (
    CASTLE_INITIAL_HEALTH,
    CASTLE_INITIAL_DAMAGE_REDUCTION,
    CASTLE_INITIAL_HEALTH_REGEN,
    CASTLE_HEALTH_UPGRADE_MULTIPLIER,
    CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER,
    CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER,
    CASTLE_HEALTH_UPGRADE_COST,
    CASTLE_DAMAGE_REDUCTION_UPGRADE_COST,
    CASTLE_HEALTH_REGEN_UPGRADE_COST,
    REF_WIDTH,
    REF_HEIGHT
)
from utils import draw_health_bar, scale_position, scale_size, scale_value

class Castle:
    """
    Represents the castle that the player defends - a defensive area where buildings and towers can be placed
    """
    def __init__(self):
        """Initialize castle with default attributes"""
        self.health = CASTLE_INITIAL_HEALTH
        self.max_health = CASTLE_INITIAL_HEALTH
        self.damage_reduction = CASTLE_INITIAL_DAMAGE_REDUCTION
        self.health_regen = CASTLE_INITIAL_HEALTH_REGEN
        self.level = 1
        
        # Track individual upgrade paths
        self.health_upgrade_level = 1
        self.damage_reduction_upgrade_level = 1
        self.health_regen_upgrade_level = 1
        
        # Define size and position in reference dimensions
        self.ref_size = (350, 150)  # Square area for placing towers and buildings
        self.ref_position = (REF_WIDTH // 2, REF_HEIGHT - self.ref_size[1] // 2 - 50)  # Bottom of the screen
        
        # Scale to actual dimensions
        self.size = scale_size(self.ref_size)
        self.position = scale_position(self.ref_position)
        
        # Create the rectangle
        self.rect = pygame.Rect(
            self.position[0] - self.size[0] // 2,
            self.position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )
    
    def update(self, dt):
        """
        Update castle state
        
        Args:
            dt: Time delta in seconds
        """
        # Regenerate health
        self.health = min(self.max_health, self.health + self.health_regen * dt)
    
    def take_damage(self, damage):
        """
        Handle incoming damage
        
        Args:
            damage: Amount of damage to take
            
        Returns:
            True if castle still has health, False if destroyed
        """
        actual_damage = damage * (1 - self.damage_reduction)
        self.health = max(0, self.health - actual_damage)
        return self.health > 0
    
    def is_position_within_castle(self, position):
        """
        Check if a position is within the castle boundaries
        
        Args:
            position: Tuple of (x, y) coordinates
            
        Returns:
            True if position is within castle boundaries, False otherwise
        """
        return self.rect.collidepoint(position)
    
    def is_on_castle_boundary(self, position, threshold=5):
        """
        Check if a position is on or near the castle boundary.
        
        Args:
            position: Tuple of (x, y) coordinates
            threshold: Distance threshold to be considered "on" the boundary
            
        Returns:
            True if position is on castle boundary, False otherwise
        """
        # Scale the threshold based on display size
        scaled_threshold = scale_value(threshold)
        
        x, y = position
        
        # Only consider positions outside the castle
        if not self.rect.collidepoint(position):
            # Check if we're near any of the edges (visually)
            
            # For the top edge - check if within horizontal bounds and near the top
            if (self.rect.left - scaled_threshold <= x <= self.rect.right + scaled_threshold and
                abs(y - self.rect.top) <= scaled_threshold):
                return True
                
            # For the left edge - check if within vertical bounds and near the left
            if (self.rect.top - scaled_threshold <= y <= self.rect.bottom + scaled_threshold and
                abs(x - self.rect.left) <= scaled_threshold):
                return True
                
            # For the right edge - check if within vertical bounds and near the right
            if (self.rect.top - scaled_threshold <= y <= self.rect.bottom + scaled_threshold and
                abs(x - self.rect.right) <= scaled_threshold):
                return True
                
            # For the bottom edge - check if within horizontal bounds and near the bottom
            if (self.rect.left - scaled_threshold <= x <= self.rect.right + scaled_threshold and
                abs(y - self.rect.bottom) <= scaled_threshold):
                return True
        
        return False
    
    def get_health_upgrade_cost(self):
        """
        Get the cost to upgrade castle max health
        
        Returns:
            Dictionary of resource costs
        """
        # Scale cost with upgrade level
        return {
            resource_type: int(amount * self.health_upgrade_level * 1.2)
            for resource_type, amount in CASTLE_HEALTH_UPGRADE_COST.items()
        }
    
    def get_damage_reduction_upgrade_cost(self):
        """
        Get the cost to upgrade castle damage reduction
        
        Returns:
            Dictionary of resource costs
        """
        # Scale cost with upgrade level
        return {
            resource_type: int(amount * self.damage_reduction_upgrade_level * 1.3)
            for resource_type, amount in CASTLE_DAMAGE_REDUCTION_UPGRADE_COST.items()
        }
    
    def get_health_regen_upgrade_cost(self):
        """
        Get the cost to upgrade castle health regeneration
        
        Returns:
            Dictionary of resource costs
        """
        # Scale cost with upgrade level
        return {
            resource_type: int(amount * self.health_regen_upgrade_level * 1.4)
            for resource_type, amount in CASTLE_HEALTH_REGEN_UPGRADE_COST.items()
        }
    
    def upgrade_health(self, resource_manager):
        """
        Upgrade castle max health
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        # Calculate upgrade cost based on health upgrade level
        cost = self.get_health_upgrade_cost()
        
        if resource_manager.spend_resources(cost):
            self.max_health *= CASTLE_HEALTH_UPGRADE_MULTIPLIER
            self.health = self.max_health  # Fully heal on upgrade
            self.level += 1
            self.health_upgrade_level += 1
            return True
        return False
    
    def upgrade_damage_reduction(self, resource_manager):
        """
        Upgrade castle damage reduction
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        # Calculate upgrade cost based on damage reduction upgrade level
        cost = self.get_damage_reduction_upgrade_cost()
        
        if resource_manager.spend_resources(cost):
            self.damage_reduction = min(0.9, self.damage_reduction * CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER)
            self.level += 1
            self.damage_reduction_upgrade_level += 1
            return True
        return False
    
    def upgrade_health_regen(self, resource_manager):
        """
        Upgrade castle health regeneration
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        # Calculate upgrade cost based on health regen upgrade level
        cost = self.get_health_regen_upgrade_cost()
        
        if resource_manager.spend_resources(cost):
            self.health_regen *= CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
            self.level += 1
            self.health_regen_upgrade_level += 1
            return True
        return False
    
    def draw(self, screen):
        """
        Draw castle to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw castle perimeter (walls)
        wall_color = (100, 100, 150)
        wall_thickness = scale_value(4)
        pygame.draw.rect(screen, wall_color, self.rect, wall_thickness)
        
        # Draw corner towers
        tower_size = scale_value(20)
        tower_color = (80, 80, 120)
        
        # Top-left tower
        pygame.draw.rect(screen, tower_color, 
                        (self.rect.left - tower_size // 2, self.rect.top - tower_size // 2, 
                        tower_size, tower_size))
        
        # Top-right tower
        pygame.draw.rect(screen, tower_color, 
                        (self.rect.right - tower_size // 2, self.rect.top - tower_size // 2, 
                        tower_size, tower_size))
        
        # Bottom-left tower
        pygame.draw.rect(screen, tower_color, 
                        (self.rect.left - tower_size // 2, self.rect.bottom - tower_size // 2, 
                        tower_size, tower_size))
        
        # Bottom-right tower
        pygame.draw.rect(screen, tower_color, 
                        (self.rect.right - tower_size // 2, self.rect.bottom - tower_size // 2, 
                        tower_size, tower_size))
        
        # Draw middle towers on each side
        pygame.draw.rect(screen, tower_color,
                        (self.rect.centerx - tower_size // 2, self.rect.top - tower_size // 2,
                        tower_size, tower_size))
        
        pygame.draw.rect(screen, tower_color,
                        (self.rect.centerx - tower_size // 2, self.rect.bottom - tower_size // 2,
                        tower_size, tower_size))
        
        pygame.draw.rect(screen, tower_color,
                        (self.rect.left - tower_size // 2, self.rect.centery - tower_size // 2,
                        tower_size, tower_size))
        
        pygame.draw.rect(screen, tower_color,
                        (self.rect.right - tower_size // 2, self.rect.centery - tower_size // 2,
                        tower_size, tower_size))
        
        # Draw castle name and level
        font_size = scale_value(24)
        font = pygame.font.Font(None, font_size)
        text = font.render(f"Castle (Level {self.level})", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - scale_value(20)))
        screen.blit(text, text_rect)
