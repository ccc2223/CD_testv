# monsters/base_monster.py
"""
Base monster class for Castle Defense
"""
import pygame
import math
from utils import draw_health_bar, scale_position, scale_size, scale_value

class Monster:
    """Base class for all monsters"""
    def __init__(self, start_pos, target_pos, monster_type, stats):
        """
        Initialize monster with position, target, and stats
        
        Args:
            start_pos: Tuple of (x, y) starting coordinates
            target_pos: Tuple of (x, y) target coordinates (castle position)
            monster_type: String indicating monster type
            stats: Dictionary of monster stats
        """
        self.position = list(start_pos)
        self.target_position = target_pos
        self.monster_type = monster_type
        
        # Set stats from config
        self.max_health = stats["health"]
        self.health = self.max_health
        self.speed = scale_value(stats["speed"])  # Scale speed based on screen size
        self.damage = stats["damage"]
        self.flying = stats.get("flying", False)
        
        # Calculate direction vector toward castle
        direction = (
            target_pos[0] - start_pos[0],
            target_pos[1] - start_pos[1]
        )
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        if length > 0:
            self.direction = (direction[0] / length, direction[1] / length)
        else:
            self.direction = (0, 1)  # Default downward if no direction
        
        # Status effects
        self.slowed = False
        self.slow_timer = 0
        self.slow_factor = 1.0
        
        # Animation flags
        self.hit_animation_timer = 0
        self.hit_flash_color = None
        
        # Visual properties - scale based on screen size
        self.ref_size = (30, 30)
        self.size = scale_size(self.ref_size)
        self.rect = pygame.Rect(
            self.position[0] - self.size[0] // 2,
            self.position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )
        self.color = self.get_color_from_type(monster_type)
        
        # Monster state flags
        self.is_dead = False
        self.reached_castle = False
        
        # Attack state properties
        self.attacking_castle = False
        self.attack_timer = 0
        self.attack_interval = 1.0  # Attack once per second
        self.attack_animation_timer = 0
        self.attack_animation_duration = 0.3  # Duration of attack animation in seconds
    
    def get_color_from_type(self, monster_type):
        """
        Get color based on monster type
        
        Args:
            monster_type: String indicating monster type
            
        Returns:
            RGB color tuple
        """
        colors = {
            "Grunt": (150, 50, 50),    # Red
            "Runner": (150, 150, 50),  # Yellow
            "Tank": (100, 100, 150),   # Blue
            "Flyer": (150, 50, 150),   # Purple
            "Force": (255, 100, 100),  # Bright red
            "Spirit": (100, 255, 100), # Bright green
            "Magic": (100, 100, 255),  # Bright blue
            "Void": (150, 0, 150)      # Deep purple
        }
        return colors.get(monster_type, (100, 100, 100))
    
    def update(self, dt, castle, animation_manager=None):
        """
        Update monster position and status effects
        
        Args:
            dt: Time delta in seconds
            castle: Castle instance to check for collision
            animation_manager: Optional AnimationManager for visual effects
            
        Returns:
            True if monster is still active, False if reached castle or dead
        """
        # Check if monster is already dead
        if self.is_dead:
            return False
            
        # Check if health is zero or below
        if self.health <= 0:
            self.is_dead = True
            return False
        
        self.update_slow(dt)
        self.update_animations(dt)
        
        # If monster is attacking castle, handle attack logic
        if self.attacking_castle:
            return self.update_castle_attack(dt, castle, animation_manager)
            
        # Move toward castle
        effective_speed = self.speed * self.slow_factor * dt
        self.position[0] += self.direction[0] * effective_speed
        self.position[1] += self.direction[1] * effective_speed
        
        # Update rectangle position
        self.rect.centerx = int(self.position[0])
        self.rect.centery = int(self.position[1])
        
        # Check if we've reached the castle boundary
        if self.is_at_castle_boundary(castle):
            # Start attacking instead of immediately being removed
            self.attacking_castle = True
            
            # Create animation for reaching castle if available
            if animation_manager:
                animation_manager.create_monster_hit_animation(self)
                
            return True  # Keep monster active while attacking
            
        # Check for status effects animations
        if animation_manager and self.slowed:
            animation_manager.update_monster_status_effects([self])
            
        return True
    
    def update_castle_attack(self, dt, castle, animation_manager=None):
        """
        Update logic for when monster is attacking the castle
        
        Args:
            dt: Time delta in seconds
            castle: Castle instance being attacked
            animation_manager: Optional AnimationManager for visual effects
            
        Returns:
            True if monster should remain active, False if it should be removed
        """
        # Update attack timer
        self.attack_timer += dt
        
        # Attack the castle at intervals
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            
            # Trigger attack animation
            self.attack_animation_timer = self.attack_animation_duration
            
            # Attack the castle
            if not castle.take_damage(self.damage):
                # Castle was destroyed
                return False
            
            # Create attack animation if available
            if animation_manager:
                animation_manager.create_castle_attack_animation(self, castle.position)
        
        # Update attack animation
        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= dt
        
        return True  # Keep monster active while attacking
    
    def is_at_castle_boundary(self, castle):
        """
        Check if monster has reached castle boundary
        
        Args:
            castle: Castle instance to check
            
        Returns:
            True if at boundary, False otherwise
        """
        return castle.is_on_castle_boundary((self.position[0], self.position[1]))
    
    def update_animations(self, dt):
        """
        Update animation timers and effects
        
        Args:
            dt: Time delta in seconds
        """
        # Update hit animation
        if self.hit_animation_timer > 0:
            self.hit_animation_timer -= dt
            if self.hit_animation_timer <= 0:
                self.hit_flash_color = None
    
    def take_damage(self, damage, damage_type=None):
        """
        Apply damage to monster and trigger hit animation
        
        Args:
            damage: Amount of damage to take
            damage_type: Type of damage for visual effects
            
        Returns:
            True if monster is still alive, False if defeated
        """
        # Don't damage dead monsters
        if self.is_dead:
            return False
            
        self.health -= damage
        
        # Set hit animation
        self.hit_animation_timer = 0.2  # Flash for 0.2 seconds
        
        # Set flash color based on damage type
        if damage_type == "frost":
            self.hit_flash_color = (100, 200, 255)  # Ice blue
        elif damage_type == "splash":
            self.hit_flash_color = (255, 150, 50)   # Orange
        else:
            self.hit_flash_color = (255, 255, 255)  # White
        
        # Check if monster was killed
        if self.health <= 0:
            self.is_dead = True
            return False
            
        return True
    
    def attack_castle(self, castle):
        """
        Attack the castle
        
        Args:
            castle: Castle instance to attack
            
        Returns:
            True if castle survived, False if destroyed
        """
        return castle.take_damage(self.damage)
    
    def apply_slow(self, slow_effect, duration):
        """
        Apply slow effect to monster
        
        Args:
            slow_effect: Amount of slow (0-1)
            duration: Duration of slow effect in seconds
        """
        self.slowed = True
        self.slow_factor = min(self.slow_factor, 1.0 - slow_effect)
        self.slow_timer = max(self.slow_timer, duration)
    
    def update_slow(self, dt):
        """
        Update slow effect duration
        
        Args:
            dt: Time delta in seconds
        """
        if self.slowed:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slowed = False
                self.slow_factor = 1.0
    
    def draw(self, screen):
        """
        Draw monster to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Don't draw dead monsters
        if self.is_dead:
            return
            
        # Determine the color to use
        if self.hit_animation_timer > 0:
            draw_color = self.hit_flash_color
        else:
            draw_color = self.color
        
        # Draw monster based on type
        if self.flying:
            # Draw circle for flying monsters
            pygame.draw.circle(screen, draw_color, 
                              (int(self.position[0]), int(self.position[1])), 
                              self.size[0] // 2)
        else:
            # Draw rectangle for ground monsters
            pygame.draw.rect(screen, draw_color, self.rect)
        
        # Draw health bar
        health_bar_pos = (self.rect.left, self.rect.top - scale_value(10))
        health_bar_size = (self.rect.width, scale_value(5))
        draw_health_bar(screen, health_bar_pos, health_bar_size, 
                       self.health, self.max_health)
        
        # Draw slow effect indicator
        if self.slowed:
            pygame.draw.circle(screen, (100, 200, 255), 
                              (int(self.position[0]), int(self.position[1])), 
                              int(self.size[0] * 0.6), scale_value(1))
        
        # Draw attack animation when attacking castle
        if self.attacking_castle and self.attack_animation_timer > 0:
            # Calculate attack animation intensity based on timer
            intensity = self.attack_animation_timer / self.attack_animation_duration
            
            # Draw an expanding circle for attack animation
            attack_radius = int(self.size[0] * 0.7 * (1 - intensity))
            
            # Create a surface with per-pixel alpha for the attack animation
            attack_surface_size = max(1, attack_radius * 2)
            attack_surface = pygame.Surface((attack_surface_size, attack_surface_size), pygame.SRCALPHA)
            
            # Calculate alpha based on remaining time
            alpha = int(200 * intensity)
            attack_color = (255, 50, 50, alpha)  # Red with fading alpha
            
            # Draw the attack circle on the surface
            pygame.draw.circle(attack_surface, attack_color, 
                             (attack_radius, attack_radius), attack_radius)
            
            # Position the attack animation centered on the monster
            attack_pos = (
                int(self.position[0] - attack_radius),
                int(self.position[1] - attack_radius)
            )
            
            # Draw the attack animation
            screen.blit(attack_surface, attack_pos)
