# monsters/boss_monster.py
"""
Boss monster implementation for Castle Defense
"""
from .base_monster import Monster
from config import BOSS_STATS, LOOT_BOSS_BASE_COIN_DROP
from utils import scale_size, scale_value

class BossMonster(Monster):
    """Special boss monster with unique abilities"""
    def __init__(self, start_pos, target_pos, boss_type):
        """
        Initialize boss monster
        
        Args:
            start_pos: Tuple of (x, y) starting coordinates
            target_pos: Tuple of (x, y) target coordinates (castle position)
            boss_type: String indicating boss type ("Force", "Spirit", etc.)
        """
        stats = BOSS_STATS.get(boss_type, {})
        super().__init__(start_pos, target_pos, boss_type, stats)
        
        # Boss-specific properties
        self.boss_type = boss_type
        self.core_drop = boss_type + " Core"
        self.special_ability = stats.get("ability", None)
        self.ability_cooldown = 10  # seconds
        self.ability_timer = self.ability_cooldown
        
        # Make boss larger
        self.ref_size = (50, 50)
        self.size = scale_size(self.ref_size)
        self.rect = pygame.Rect(
            self.position[0] - self.size[0] // 2,
            self.position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )
        
        # Boss animation flags
        self.ability_animation_timer = 0
        
        # Boss attack properties - stronger attacks, slower interval
        self.attack_interval = 1.5  # Attack every 1.5 seconds (slower but stronger)
    
    def update(self, dt, castle, animation_manager=None):
        """
        Update boss position, status effects, and ability
        
        Args:
            dt: Time delta in seconds
            castle: Castle instance to check for collision
            animation_manager: Optional AnimationManager for visual effects
            
        Returns:
            True if boss is still active, False if reached castle
        """
        # Check if boss is already dead or at castle
        if self.is_dead:
            return False
        
        # Only update special ability if not attacking castle
        if not self.attacking_castle:
            # Update ability cooldown
            self.ability_timer -= dt
            if self.ability_timer <= 0:
                self.use_special_ability(animation_manager)
                self.ability_timer = self.ability_cooldown
                
                # Set ability animation
                self.ability_animation_timer = 0.5  # Animation duration
        
        # Update ability animation
        if self.ability_animation_timer > 0:
            self.ability_animation_timer -= dt
        
        # Call parent update
        return super().update(dt, castle, animation_manager)
    
    def use_special_ability(self, animation_manager=None):
        """
        Use boss's special ability based on type
        
        Args:
            animation_manager: Optional AnimationManager for visual effects
        """
        if self.special_ability == "heal":
            # Heal 10% of max health
            self.health = min(self.max_health, self.health + self.max_health * 0.1)
            
            # Create heal animation
            if animation_manager:
                # Could add heal animation here
                pass
        
        elif self.special_ability == "knockback":
            # Knockback ability would be implemented here
            # This would need to interact with the WaveManager to affect other monsters
            pass
        
        elif self.special_ability == "teleport":
            # Teleport ability would be implemented here
            # Could change the boss's position drastically
            pass
        
        elif self.special_ability == "spawn":
            # Spawn ability would be implemented here
            # This would need to interact with the WaveManager to spawn minions
            pass
    
    def drop_loot(self):
        """
        Generate loot when boss is defeated
        
        Returns:
            Dictionary of resources and amounts
        """
        return {
            "Monster Coins": LOOT_BOSS_BASE_COIN_DROP,
            self.core_drop: 1
        }
    
    def draw(self, screen):
        """
        Draw boss to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Don't draw dead bosses
        if self.is_dead:
            return
            
        super().draw(screen)
        
        # Draw boss indicator (crown)
        crown_points = [
            (self.position[0], self.position[1] - self.size[1] // 2 - scale_value(10)),
            (self.position[0] - scale_value(10), self.position[1] - self.size[1] // 2),
            (self.position[0] + scale_value(10), self.position[1] - self.size[1] // 2)
        ]
        
        # Make crown flash when using ability
        crown_color = (255, 255, 200) if self.ability_animation_timer > 0 else (255, 215, 0)
        pygame.draw.polygon(screen, crown_color, crown_points)

# Make sure to import pygame for drawing operations
import pygame
