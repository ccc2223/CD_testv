# effects/animation_manager.py
"""
Animation manager for creating and managing visual effects in Castle Defense
"""
import pygame
from effects.particles import (
    ParticleSystem,
    create_arrow_effect,
    create_sniper_shot_effect,
    create_splash_effect,
    create_freeze_effect,
    create_monster_hit_effect,
    create_monster_death_effect,
    create_slow_effect_particles,
    create_castle_attack_effect  # New effect for castle attacks
)

class AnimationManager:
    """Manages all animations and visual effects in the game"""
    def __init__(self):
        """Initialize animation manager with empty particle systems"""
        self.particle_system = ParticleSystem()
        self.active_animations = []
    
    def update(self, dt):
        """
        Update all animations and particle systems
        
        Args:
            dt: Time delta in seconds
        """
        # Update particle system
        self.particle_system.update(dt)
        
        # Update and remove completed animations
        self.active_animations = [anim for anim in self.active_animations if anim.update(dt)]
    
    def draw(self, screen):
        """
        Draw all animations and particle systems
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw particle system
        self.particle_system.draw(screen)
    
    def clear(self):
        """Clear all animations and particles"""
        self.particle_system.clear()
        self.active_animations = []
    
    # Tower attack animations
    def create_tower_attack_animation(self, tower, target):
        """
        Create appropriate attack animation based on tower type
        
        Args:
            tower: Tower that is attacking
            target: Monster that is being attacked
        """
        tower_pos = tower.position
        target_pos = target.position
        
        # Check if tower has item effects for enhanced visuals
        enhanced_visuals = tower.has_item_effects
        
        if tower.tower_type == "Archer":
            if enhanced_visuals and tower.splash_damage_enabled:
                # Enhanced arrows for Unstoppable Force item
                create_arrow_effect(tower_pos, target_pos, self.particle_system, enhanced=True)
            else:
                create_arrow_effect(tower_pos, target_pos, self.particle_system)
        
        elif tower.tower_type == "Sniper":
            if enhanced_visuals and tower.splash_damage_enabled:
                # Enhanced sniper shot for Unstoppable Force item
                create_sniper_shot_effect(tower_pos, target_pos, self.particle_system, enhanced=True)
            else:
                create_sniper_shot_effect(tower_pos, target_pos, self.particle_system)
        
        elif tower.tower_type == "Splash":
            # For splash tower, first send a projectile, then create explosion
            create_arrow_effect(tower_pos, target_pos, self.particle_system)
            
            # Create larger explosion if tower has Unstoppable Force
            if enhanced_visuals:
                # Enhanced explosion with more particles
                create_splash_effect(target_pos, tower.aoe_radius / 2, self.particle_system, enhanced=True)
            else:
                create_splash_effect(target_pos, tower.aoe_radius / 2, self.particle_system)
        
        elif tower.tower_type == "Frozen":
            if enhanced_visuals:
                # Enhanced freeze effect for Unstoppable Force
                create_freeze_effect(target_pos, tower.range / 4, self.particle_system, enhanced=True)
            else:
                create_freeze_effect(target_pos, tower.range / 4, self.particle_system)
    
    # Monster effect animations
    def create_monster_hit_animation(self, monster, damage_type=None):
        """
        Create hit effect when monster takes damage
        
        Args:
            monster: Monster that was hit
            damage_type: Type of damage (optional, for different color effects)
        """
        position = monster.position
        
        # Default color based on damage type, or red if none specified
        if damage_type == "frost":
            color = (100, 200, 255)  # Ice blue
        elif damage_type == "splash":
            color = (255, 150, 50)   # Orange
        else:
            color = (255, 0, 0)      # Red
            
        create_monster_hit_effect(position, self.particle_system, color)
    
    def create_monster_death_animation(self, monster):
        """
        Create death effect when monster is killed
        
        Args:
            monster: Monster that was killed
        """
        # Use monster's size and color for appropriate effect
        position = monster.position
        size = max(monster.size[0], monster.size[1])  # Use larger dimension
        create_monster_death_effect(position, size, self.particle_system, monster.color)
    
    # NEW: Create a castle attack animation
    def create_castle_attack_animation(self, monster, castle_position):
        """
        Create animation for monster attacking castle
        
        Args:
            monster: Monster that is attacking
            castle_position: Position on castle being attacked
        """
        # Pass the monster's position and the castle position to show attack
        create_castle_attack_effect(
            monster.position, 
            castle_position, 
            self.particle_system, 
            monster.color
        )
    
    # Status effect animations
    def update_monster_status_effects(self, monsters):
        """
        Update visual effects for monster status effects
        
        Args:
            monsters: List of active monsters to check for status effects
        """
        for monster in monsters:
            if monster.slowed:
                # Create slow effect particles for slowed monsters
                create_slow_effect_particles(monster.position, self.particle_system)
