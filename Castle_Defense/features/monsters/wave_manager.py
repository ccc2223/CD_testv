# features/monsters/wave_manager.py
"""
Wave management system for Castle Defense
"""
import pygame
import random
import math
from .factory import MonsterFactory
from .boss_monster import BossMonster
from config import (
    MONSTER_STATS,
    BOSS_STATS,
    MONSTER_SPAWN_INTERVAL,
    WAVE_DIFFICULTY_MULTIPLIER,
    WAVE_MONSTER_COUNT_BASE,
    WAVE_MONSTER_COUNT_MULTIPLIER,
    REF_WIDTH,
    REF_HEIGHT
)
from utils import scale_position

class WaveManager:
    """Manages monster waves and spawning"""
    def __init__(self):
        """Initialize wave manager"""
        self.current_wave = 0
        self.active_monsters = []
        self.spawn_timer = 0
        self.monsters_to_spawn = 0
        self.wave_active = False
        self.wave_completed = True
        
        # Animation flags
        self.wave_start_animation_timer = 0
        self.wave_complete_animation_timer = 0
        
        # Spawn points will be generated dynamically across the top of the screen
        self.spawn_path = []  # No longer used with the direct movement system
        
        # Developer mode settings - Set continuous_wave to True by default
        self.continuous_wave = True  # Auto-start next wave when current wave ends
    
    def start_next_wave(self):
        """
        Start the next wave of monsters
        
        Returns:
            True if wave was started, False if already active
        """
        if not self.wave_active:
            self.current_wave += 1
            self.wave_active = True
            self.wave_completed = False
            self.spawn_timer = 0
            
            # Set wave start animation
            self.wave_start_animation_timer = 1.0  # 1 second animation
            
            # Calculate number of monsters to spawn
            if self.current_wave % 10 == 0:
                # Boss wave
                self.monsters_to_spawn = 1
            else:
                # Regular wave
                base_count = WAVE_MONSTER_COUNT_BASE
                multiplier = WAVE_MONSTER_COUNT_MULTIPLIER ** (self.current_wave // 10)
                self.monsters_to_spawn = int(base_count + self.current_wave * 0.5 * multiplier)
            
            return True
        return False
    
    def update(self, dt, castle, animation_manager=None):
        """
        Update wave state and all active monsters
        
        Args:
            dt: Time delta in seconds
            castle: Castle instance for monster attacks
            animation_manager: Optional AnimationManager for visual effects
        """
        # Update animation timers
        if self.wave_start_animation_timer > 0:
            self.wave_start_animation_timer -= dt
        
        if self.wave_complete_animation_timer > 0:
            self.wave_complete_animation_timer -= dt
        
        if self.wave_active:
            # Spawn new monsters
            self.spawn_timer += dt
            if self.spawn_timer >= MONSTER_SPAWN_INTERVAL and self.monsters_to_spawn > 0:
                self.spawn_monster(castle.position, animation_manager)
                self.monsters_to_spawn -= 1
                self.spawn_timer = 0
            
            # Update all active monsters and handle dead monsters
            monsters_to_remove = []
            
            for monster in self.active_monsters:
                monster_still_active = monster.update(dt, castle, animation_manager)
                
                if not monster_still_active:
                    # Monster died
                    monsters_to_remove.append(monster)
            
            # Remove monsters
            for monster in monsters_to_remove:
                if monster in self.active_monsters:
                    # If monster died but wasn't handled by a tower, handle it here
                    if monster.is_dead and not monster.reached_castle:
                        # Get game_instance reference to access resource_manager
                        # This is a fallback - towers should normally handle this
                        from game import game_instance
                        if game_instance:
                            self.handle_monster_death(monster, game_instance.resource_manager, animation_manager)
                    
                    self.active_monsters.remove(monster)
            
            # Check if wave is complete
            if len(self.active_monsters) == 0 and self.monsters_to_spawn == 0:
                self.wave_active = False
                self.wave_completed = True
                self.wave_complete_animation_timer = 2.0  # 2 second animation
    
    def spawn_monster(self, castle_position, animation_manager=None):
        """
        Spawn a monster based on current wave
        
        Args:
            castle_position: Position of castle to target
            animation_manager: Optional AnimationManager for visual effects
        """
        # Generate random spawn position along the top of the screen in reference coordinates
        ref_spawn_x = random.randint(50, REF_WIDTH - 50)
        ref_spawn_y = 50  # 50 pixels from the top
        
        # Scale to actual screen coordinates
        spawn_pos = scale_position((ref_spawn_x, ref_spawn_y))
        
        if self.current_wave % 10 == 0:
            # Boss wave
            boss_type = self.get_boss_type()
            monster = MonsterFactory.create_boss_monster(boss_type, spawn_pos, castle_position)
        else:
            # Regular monster
            monster_type = self.get_random_monster_type()
            monster = MonsterFactory.create_regular_monster(monster_type, spawn_pos, castle_position, self.current_wave)
        
        self.active_monsters.append(monster)
        
        # Create spawn animation if animation manager is provided
        # This would be implemented in the animation_manager
    
    def get_boss_type(self):
        """
        Determine boss type based on wave number
        
        Returns:
            String boss type
        """
        boss_types = ["Force", "Spirit", "Magic", "Void"]
        return boss_types[(self.current_wave // 10 - 1) % len(boss_types)]
    
    def get_random_monster_type(self):
        """
        Get a random monster type weighted by wave number
        
        Returns:
            String monster type
        """
        available_types = []
        
        # Always include Grunt
        available_types.append("Grunt")
        
        # Add Runner after wave 3
        if self.current_wave >= 3:
            available_types.append("Runner")
        
        # Add Tank after wave 5
        if self.current_wave >= 5:
            available_types.append("Tank")
        
        # Add Flyer after wave 8
        if self.current_wave >= 8:
            available_types.append("Flyer")
        
        # Weight later monsters to be more common in later waves
        # Using int() to ensure all weights are integers
        weights = {
            "Grunt": int(100 - min(80, self.current_wave * 2)),
            "Runner": int(min(60, max(10, self.current_wave * 3))),
            "Tank": int(min(50, max(10, self.current_wave * 2))),
            "Flyer": int(min(40, max(10, self.current_wave * 1.5)))
        }
        
        # Filter weights to only include available types
        weights = {k: v for k, v in weights.items() if k in available_types}
        
        # Choose random type based on weights
        total_weight = sum(weights.values())
        
        # Ensure total_weight is at least 1
        if total_weight <= 0:
            return "Grunt"  # Default to Grunt if weights calculation went wrong
        
        r = random.randint(1, total_weight)
        cumulative_weight = 0
        
        for monster_type, weight in weights.items():
            cumulative_weight += weight
            if r <= cumulative_weight:
                return monster_type
        
        # Fallback
        return "Grunt"
    
    def handle_monster_death(self, monster, resource_manager, animation_manager=None):
        """
        Handle monster death and loot drops
        
        Args:
            monster: Monster that died
            resource_manager: ResourceManager to add loot
            animation_manager: Optional AnimationManager for visual effects
        """
        # Already dead or not in active monsters
        if not monster or not monster in self.active_monsters:
            return
            
        # Mark as dead to prevent duplicate handling
        monster.is_dead = True
            
        # Create death animation if animation manager is provided
        if animation_manager:
            animation_manager.create_monster_death_animation(monster)
        
        # Add Monster Coins for all monsters
        resource_manager.add_resource("Monster Coins", 1)
        
        # Handle boss loot
        if isinstance(monster, BossMonster):
            loot = monster.drop_loot()
            for resource_type, amount in loot.items():
                resource_manager.add_resource(resource_type, amount)
    
    def draw(self, screen):
        """
        Draw all monsters and wave animations
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw all monsters
        for monster in self.active_monsters:
            monster.draw(screen)
        
        # Draw wave start animation
        if self.wave_start_animation_timer > 0:
            alpha = int(255 * min(1, self.wave_start_animation_timer))
            font_size = 36
            font = pygame.font.Font(None, font_size)
            
            if self.current_wave % 10 == 0:
                # Boss wave announcement
                text = f"BOSS WAVE {self.current_wave}"
                color = (255, 100, 100)  # Red for boss waves
            else:
                # Regular wave announcement
                text = f"Wave {self.current_wave}"
                color = (255, 255, 255)
            
            text_surface = font.render(text, True, color)
            
            # Apply fading effect
            if alpha < 255:
                alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, alpha))
                text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 100))
            screen.blit(text_surface, text_rect)
        
        # Draw wave complete animation
        if self.wave_complete_animation_timer > 0 and self.wave_completed:
            alpha = int(255 * min(1, self.wave_complete_animation_timer))
            font_size = 30
            font = pygame.font.Font(None, font_size)
            
            text = f"Wave {self.current_wave} Complete!"
            text_surface = font.render(text, True, (200, 255, 200))
            
            # Apply fading effect
            if alpha < 255:
                alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                alpha_surface.fill((255, 255, 255, alpha))
                text_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 150))
            screen.blit(text_surface, text_rect)
            
            # Draw continuous wave mode indicator if enabled
            if self.continuous_wave:
                font_size = 20
                font = pygame.font.Font(None, font_size)
                
                next_wave_text = f"Starting Wave {self.current_wave + 1} Soon..."
                next_wave_surface = font.render(next_wave_text, True, (200, 200, 255))
                
                # Apply fading effect
                if alpha < 255:
                    alpha_surface = pygame.Surface(next_wave_surface.get_size(), pygame.SRCALPHA)
                    alpha_surface.fill((255, 255, 255, alpha))
                    next_wave_surface.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                next_wave_rect = next_wave_surface.get_rect(center=(screen.get_width() // 2, 180))
                screen.blit(next_wave_surface, next_wave_rect)
