# towers/splash_tower.py
"""
Splash Tower implementation for Castle Defense
"""
from .base_tower import Tower
from config import (
    TOWER_TYPES,
    TOWER_UPGRADE_COST_MULTIPLIER,
    TOWER_MONSTER_COIN_COSTS,
    TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
    TOWER_AOE_UPGRADE_MULTIPLIER
)

class SplashTower(Tower):
    """Tower with area damage"""
    def __init__(self, position):
        super().__init__(position, "Splash")
    
    def attack(self, animation_manager=None):
        """
        Attack all targets within AoE radius of primary target
        
        Args:
            animation_manager: Optional AnimationManager for visual effects
        """
        super().attack(animation_manager)
        
        if not self.targets:
            return
            
        primary_target = self.targets[0]
        primary_target_pos = primary_target.position
        
        # Create attack animation before potentially killing monsters
        if animation_manager:
            animation_manager.create_tower_attack_animation(self, primary_target)
        
        # Store monsters that were killed for handling after damage loop
        killed_monsters = []
        
        # Deal damage to all monsters within AoE radius of primary target
        for monster in self.targets:
            if monster.is_dead:
                continue
                
            if distance(monster.position, primary_target_pos) <= self.aoe_radius:
                if not monster.take_damage(self.damage, "splash"):
                    # Monster was killed
                    killed_monsters.append(monster)
                else:
                    # Monster was hit but not killed
                    if animation_manager:
                        animation_manager.create_monster_hit_animation(monster, "splash")
        
        # Handle killed monsters
        if killed_monsters:
            # Get reference to wave_manager and resource_manager from the game instance
            from game import Game
            for game_instance in [obj for obj in globals().values() if isinstance(obj, Game)]:
                for monster in killed_monsters:
                    if animation_manager:
                        animation_manager.create_monster_death_animation(monster)
                    game_instance.wave_manager.handle_monster_death(monster, game_instance.resource_manager, animation_manager)
    
    def calculate_aoe_radius_upgrade_cost(self):
        """
        Calculate upgrade cost for AoE radius based on AoE radius level
        
        Returns:
            Dictionary of resource costs
        """
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with AoE radius level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.aoe_radius_level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def calculate_aoe_radius_upgrade_monster_coin_cost(self):
        """
        Calculate Monster Coin cost for AoE radius upgrade based on AoE radius level
        
        Returns:
            Integer Monster Coin cost
        """
        base_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 15)  # Higher base for Splash tower
        return int(base_cost * (TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER ** (self.aoe_radius_level - 1)))
    
    def upgrade_aoe_radius(self, resource_manager):
        """
        Upgrade tower AoE radius
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        cost = self.calculate_aoe_radius_upgrade_cost()
        monster_coin_cost = self.calculate_aoe_radius_upgrade_monster_coin_cost()
        
        # Check if we have enough resources and Monster Coins
        if not resource_manager.has_resources(cost) or resource_manager.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        # Spend resources and Monster Coins
        if resource_manager and resource_manager.spend_resources(cost):
            # Spend the Monster Coins separately
            resource_manager.spend_resource("Monster Coins", monster_coin_cost)
            
            # Upgrade both reference and scaled AoE radius
            self.base_ref_aoe_radius *= TOWER_AOE_UPGRADE_MULTIPLIER
            self.base_aoe_radius = scale_value(self.base_ref_aoe_radius)
            self.aoe_radius_level += 1
            self.level += 1  # Keep overall level for compatibility
            self.apply_item_effects()  # Re-apply item effects after upgrade
            return True
        return False
    
    def draw(self, screen):
        """
        Draw splash tower with AoE indicator
        
        Args:
            screen: Pygame surface to draw on
        """
        super().draw(screen)

# Import these at the module level to avoid circular imports in methods
from utils import distance, scale_value
