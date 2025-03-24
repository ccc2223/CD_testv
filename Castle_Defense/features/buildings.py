# features/buildings.py
"""
Building implementations for the Castle Defense game
"""
import pygame
from config import (
    MINE_INITIAL_PRODUCTION,
    MINE_PRODUCTION_INTERVAL,
    MINE_PRODUCTION_MULTIPLIER,
    MINE_UPGRADE_TIME_MULTIPLIER,
    MINE_INITIAL_UPGRADE_TIME,
    MINE_UPGRADE_COST,
    CORESMITH_CRAFTING_TIME,
    ITEM_COSTS
)
from utils import draw_health_bar

class Building:
    """Base class for all buildings"""
    def __init__(self, position):
        """
        Initialize building with position
        
        Args:
            position: Tuple of (x, y) coordinates
        """
        self.position = position
        self.level = 1
        self.size = (50, 50)
        self.rect = pygame.Rect(
            position[0] - self.size[0] // 2,
            position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )
        self.color = (100, 100, 100)  # Default color
    
    def update(self, dt, resource_manager, raw_dt=None, game_paused=False):
        """
        Update building state
        
        Args:
            dt: Time delta in seconds (scaled by game speed)
            resource_manager: ResourceManager for adding/spending resources
            raw_dt: Raw time delta in seconds (unaffected by game speed)
            game_paused: Boolean indicating if the game is paused
        """
        pass
    
    def draw(self, screen):
        """
        Draw building to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw level
        font = pygame.font.Font(None, 20)
        text = font.render(f"Lv {self.level}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text, text_rect)

class Mine(Building):
    """Resource-producing building"""
    def __init__(self, position):
        """
        Initialize mine with position
        
        Args:
            position: Tuple of (x, y) coordinates
        """
        super().__init__(position)
        self.resource_type = "Stone"
        self.production_rate = MINE_INITIAL_PRODUCTION
        self.production_timer = 0
        self.upgrade_timer = 0
        self.upgrading = False
        self.upgrade_time = MINE_INITIAL_UPGRADE_TIME
        self.color = (70, 70, 50)  # Brown-ish color
    
    def update(self, dt, resource_manager, raw_dt=None, game_paused=False):
        """
        Update mine state - produce resources or progress upgrade
        Always use unscaled time (raw_dt) for consistent production regardless of game speed
        
        Args:
            dt: Time delta in seconds (scaled by game speed)
            resource_manager: ResourceManager for adding resources
            raw_dt: Raw time delta in seconds (unaffected by game speed)
            game_paused: Boolean indicating if the game is paused
        """
        # If game is paused, don't update
        if game_paused:
            return
            
        # Always use raw_dt (unscaled time) for buildings to maintain consistent production
        # If raw_dt is not provided, use dt (but this should always be provided)
        actual_dt = raw_dt if raw_dt is not None else dt
        
        if self.upgrading:
            self.update_upgrade(actual_dt)
        else:
            self.update_production(actual_dt, resource_manager)
    
    def update_production(self, dt, resource_manager):
        """
        Update resource production
        
        Args:
            dt: Time delta in seconds
            resource_manager: ResourceManager for adding resources
        """
        self.production_timer += dt
        if self.production_timer >= MINE_PRODUCTION_INTERVAL:
            self.production_timer = 0
            resource_manager.add_resource(self.resource_type, self.production_rate)
    
    def update_upgrade(self, dt):
        """
        Update upgrade progress
        
        Args:
            dt: Time delta in seconds
        """
        self.upgrade_timer += dt
        if self.upgrade_timer >= self.upgrade_time:
            self.complete_upgrade()
    
    def get_upgrade_cost(self):
        """
        Get the cost to upgrade this mine
        
        Returns:
            Dictionary of resource costs
        """
        return MINE_UPGRADE_COST
    
    def start_upgrade(self, resource_manager):
        """
        Start upgrading the mine
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade started, False if insufficient resources
        """
        if self.upgrading:
            return False
        
        upgrade_cost = self.get_upgrade_cost()
        if resource_manager.spend_resources(upgrade_cost):
            self.upgrading = True
            self.upgrade_timer = 0
            return True
        return False
    
    def complete_upgrade(self):
        """Complete the upgrade and update mine stats"""
        self.level += 1
        self.upgrading = False
        self.upgrade_timer = 0
        self.update_resource_type()
        self.production_rate *= MINE_PRODUCTION_MULTIPLIER
        self.upgrade_time *= MINE_UPGRADE_TIME_MULTIPLIER
    
    def update_resource_type(self):
        """Update resource type based on mine level"""
        if self.level >= 30:
            self.resource_type = "Thorium"
            self.color = (150, 200, 150)  # Greenish for Thorium
        elif self.level >= 20:
            self.resource_type = "Copper"
            self.color = (180, 100, 50)  # Copper color
        elif self.level >= 10:
            self.resource_type = "Iron"
            self.color = (100, 100, 120)  # Iron color
    
    def draw(self, screen):
        """
        Draw mine to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        super().draw(screen)
        
        # Draw resource type
        font = pygame.font.Font(None, 16)
        text = font.render(self.resource_type, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        screen.blit(text, text_rect)
        
        # Draw production progress bar above the mine
        if not self.upgrading:
            progress_pos = (self.rect.left, self.rect.top - 25)
            progress_size = (self.rect.width, 5)
            production_progress = self.production_timer / MINE_PRODUCTION_INTERVAL
            
            # Choose color based on resource type
            if self.resource_type == "Stone":
                progress_color = (180, 180, 180)  # Gray for Stone
            elif self.resource_type == "Iron":
                progress_color = (150, 150, 200)  # Bluish for Iron
            elif self.resource_type == "Copper":
                progress_color = (200, 120, 50)    # Orange for Copper
            elif self.resource_type == "Thorium":
                progress_color = (100, 220, 100)   # Green for Thorium
            else:
                progress_color = (200, 200, 200)   # Default color
                
            # Draw the production progress bar
            draw_health_bar(screen, progress_pos, progress_size, 
                            production_progress, 1.0, 
                            color=progress_color, bg_color=(50, 50, 50))
                            
            # Draw a small label for the progress bar
            small_font = pygame.font.Font(None, 12)
            progress_text = f"Mining: {int(production_progress * 100)}%"
            progress_label = small_font.render(progress_text, True, (200, 200, 200))
            label_rect = progress_label.get_rect(bottomright=(self.rect.right, self.rect.top - 27))
            screen.blit(progress_label, label_rect)
        
        # Draw upgrade progress bar if upgrading
        if self.upgrading:
            progress_pos = (self.rect.left, self.rect.bottom + 5)
            progress_size = (self.rect.width, 5)
            draw_health_bar(screen, progress_pos, progress_size, 
                           self.upgrade_timer, self.upgrade_time, 
                           color=(0, 200, 255), bg_color=(50, 50, 50))
            
            # Add upgrade progress percentage text
            upgrade_pct = int((self.upgrade_timer / self.upgrade_time) * 100)
            upgrade_text = f"Upgrading: {upgrade_pct}%"
            upgrade_label = font.render(upgrade_text, True, (0, 200, 255))
            upgrade_rect = upgrade_label.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
            screen.blit(upgrade_label, upgrade_rect)

class Coresmith(Building):
    """Building for crafting items"""
    def __init__(self, position):
        """
        Initialize coresmith with position
        
        Args:
            position: Tuple of (x, y) coordinates
        """
        super().__init__(position)
        self.crafting = False
        self.crafting_timer = 0
        self.crafting_time = CORESMITH_CRAFTING_TIME
        self.current_item = None
        self.color = (50, 80, 100)  # Bluish color
    
    def update(self, dt, resource_manager, raw_dt=None, game_paused=False):
        """
        Update coresmith state - progress crafting
        Always use unscaled time (raw_dt) for consistent crafting regardless of game speed
        
        Args:
            dt: Time delta in seconds (scaled by game speed)
            resource_manager: ResourceManager for adding crafted items
            raw_dt: Raw time delta in seconds (unaffected by game speed)
            game_paused: Boolean indicating if the game is paused
        """
        # If game is paused, don't update
        if game_paused:
            return
            
        # Always use raw_dt (unscaled time) for buildings to maintain consistent production
        # If raw_dt is not provided, use dt (but this should always be provided)
        actual_dt = raw_dt if raw_dt is not None else dt
        
        if self.crafting:
            self.crafting_timer += actual_dt
            if self.crafting_timer >= self.crafting_time:
                self.complete_crafting(resource_manager)
    
    def start_crafting(self, item_type, resource_manager):
        """
        Start crafting an item
        
        Args:
            item_type: Type of item to craft
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if crafting started, False if insufficient resources
        """
        if self.crafting:
            return False
        
        if item_type not in ITEM_COSTS:
            return False
        
        if resource_manager.spend_resources(ITEM_COSTS[item_type]):
            self.crafting = True
            self.current_item = item_type
            self.crafting_timer = 0
            return True
        return False
    
    def complete_crafting(self, resource_manager):
        """
        Complete crafting and add item to inventory
        
        Args:
            resource_manager: ResourceManager to add crafted item
        """
        if self.current_item:
            resource_manager.add_resource(self.current_item, 1)
            self.crafting = False
            self.current_item = None
            self.crafting_timer = 0
    
    def draw(self, screen):
        """
        Draw coresmith to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        super().draw(screen)
        
        # Draw "Coresmith" label
        font = pygame.font.Font(None, 16)
        text = font.render("Coresmith", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        screen.blit(text, text_rect)
        
        # Draw progress bar if crafting
        if self.crafting:
            progress_pos = (self.rect.left, self.rect.bottom + 5)
            progress_size = (self.rect.width, 5)
            draw_health_bar(screen, progress_pos, progress_size, 
                           self.crafting_timer, self.crafting_time, 
                           color=(255, 200, 0), bg_color=(50, 50, 50))
            
            # Draw item being crafted
            text = font.render(f"Crafting: {self.current_item}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
            screen.blit(text, text_rect)
            
            # Add crafting progress percentage
            crafting_pct = int((self.crafting_timer / self.crafting_time) * 100)
            pct_text = f"{crafting_pct}% Complete"
            pct_surface = font.render(pct_text, True, (255, 200, 0))
            pct_rect = pct_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 40))
            screen.blit(pct_surface, pct_rect)

class CastleUpgradeStation(Building):
    """Station for upgrading the castle"""
    def __init__(self, position):
        """
        Initialize castle upgrade station
        
        Args:
            position: Tuple of (x, y) coordinates
        """
        super().__init__(position)
        self.color = (120, 100, 140)  # Purple-ish color
    
    def update(self, dt, resource_manager, raw_dt=None, game_paused=False):
        """
        Update castle upgrade station - nothing to do in update
        
        Args:
            dt: Time delta in seconds
            resource_manager: ResourceManager (not used)
            raw_dt: Raw time delta in seconds (unaffected by game speed)
            game_paused: Boolean indicating if the game is paused
        """
        pass  # No regular updates needed
    
    def draw(self, screen):
        """
        Draw castle upgrade station to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw base
        super().draw(screen)
        
        # Draw "Castle Upgrades" label
        font = pygame.font.Font(None, 16)
        text = font.render("Castle Upgrades", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        screen.blit(text, text_rect)
        
        # Draw castle icon on the building
        castle_icon_size = 20
        castle_icon = pygame.Rect(
            self.rect.centerx - castle_icon_size // 2,
            self.rect.centery - castle_icon_size // 2,
            castle_icon_size,
            castle_icon_size
        )
        
        # Draw small castle shape
        pygame.draw.rect(screen, (180, 180, 220), castle_icon)
        
        # Draw castle turrets
        turret_size = 6
        # Top left turret
        pygame.draw.rect(screen, (160, 160, 200),
                        (castle_icon.left - turret_size // 2, 
                         castle_icon.top - turret_size // 2,
                         turret_size, turret_size))
        
        # Top right turret
        pygame.draw.rect(screen, (160, 160, 200),
                        (castle_icon.right - turret_size // 2, 
                         castle_icon.top - turret_size // 2,
                         turret_size, turret_size))
