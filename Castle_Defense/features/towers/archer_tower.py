# towers/archer_tower.py
"""
Archer Tower implementation for Castle Defense
"""
from .base_tower import Tower

class ArcherTower(Tower):
    """Tower with fast attack speed, low damage"""
    def __init__(self, position):
        super().__init__(position, "Archer")
    
    def attack(self, animation_manager=None):
        """
        Attack closest target with single-target damage
        
        Args:
            animation_manager: Optional AnimationManager for visual effects
        """
        super().attack(animation_manager)
        
        if not self.targets:
            return
            
        target = self.targets[0]  # Attack closest target
        
        if target.is_dead:
            return
        
        # Create attack animation before potentially killing the monster
        if animation_manager:
            animation_manager.create_tower_attack_animation(self, target)
        
        # Apply damage to primary target
        primary_target_killed = not target.take_damage(self.damage)
        
        # Apply splash damage if enabled (from Unstoppable Force item)
        splash_targets = []
        if self.splash_damage_enabled and self.splash_damage_radius > 0:
            for monster in self.targets:
                if monster != target and not monster.is_dead:
                    # Check if monster is within splash radius of primary target
                    if distance(monster.position, target.position) <= self.splash_damage_radius:
                        # Apply 50% damage to splash targets
                        splash_damage = self.damage * 0.5
                        if not monster.take_damage(splash_damage, "splash"):
                            # Monster was killed by splash damage
                            splash_targets.append(monster)
                        elif animation_manager:
                            # Monster was hit but not killed by splash
                            animation_manager.create_monster_hit_animation(monster, "splash")
        
        # Handle deaths and resource drops
        killed_monsters = []
        
        # Add primary target if killed
        if primary_target_killed:
            killed_monsters.append(target)
            
        # Add splash targets that were killed
        killed_monsters.extend(splash_targets)
        
        # Handle all killed monsters
        if killed_monsters:
            # Get reference to wave_manager and resource_manager from the game instance
            from game import Game
            for game_instance in [obj for obj in globals().values() if isinstance(obj, Game)]:
                for monster in killed_monsters:
                    if animation_manager:
                        animation_manager.create_monster_death_animation(monster)
                    game_instance.wave_manager.handle_monster_death(monster, game_instance.resource_manager, animation_manager)
        elif animation_manager and not primary_target_killed:
            # Primary target still alive, create hit animation
            animation_manager.create_monster_hit_animation(target)

# Import this at the module level to avoid circular import in attack()
from utils import distance
