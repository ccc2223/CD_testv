# towers/frozen_tower.py
"""
Frozen Tower implementation for Castle Defense
"""
from .base_tower import Tower
from config import (
    TOWER_TYPES,
    TOWER_UPGRADE_COST_MULTIPLIER,
    TOWER_MONSTER_COIN_COSTS,
    TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER
)

class FrozenTower(Tower):
    """Tower that slows and damages targets"""
    def __init__(self, position):
        super().__init__(position, "Frozen")
    
    def attack(self, animation_manager=None):
        """
        Attack and slow all targets in range
        
        Args:
            animation_manager: Optional AnimationManager for visual effects
        """
        super().attack(animation_manager)
        
        # Store monsters that were killed for handling after damage loop
        killed_monsters = []
        
        for target in self.targets:
            if target.is_dead:
                continue
                
            # Create attack animation
            if animation_manager:
                animation_manager.create_tower_attack_animation(self, target)
            
            # Apply damage and slow effect
            if not target.take_damage(self.damage, "frost"):
                # Monster was killed
                killed_monsters.append(target)
            else:
                # Monster was hit but not killed
                if animation_manager:
                    animation_manager.create_monster_hit_animation(target, "frost")
                
                # Apply slow effect
                target.apply_slow(self.slow_effect, self.slow_duration)
        
        # Handle killed monsters
        if killed_monsters:
            # Get reference to wave_manager and resource_manager from the game instance
            from game import Game
            for game_instance in [obj for obj in globals().values() if isinstance(obj, Game)]:
                for monster in killed_monsters:
                    if animation_manager:
                        animation_manager.create_monster_death_animation(monster)
                    game_instance.wave_manager.handle_monster_death(monster, game_instance.resource_manager, animation_manager)
    
    def calculate_slow_effect_upgrade_cost(self):
        """
        Calculate upgrade cost for slow effect based on slow effect level
        
        Returns:
            Dictionary of resource costs
        """
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with slow effect level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.slow_effect_level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def calculate_slow_effect_upgrade_monster_coin_cost(self):
        """
        Calculate Monster Coin cost for slow effect upgrade based on slow effect level
        
        Returns:
            Integer Monster Coin cost
        """
        base_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 15)  # Higher base for Frozen tower
        return int(base_cost * (TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER ** (self.slow_effect_level - 1)))
    
    def calculate_slow_duration_upgrade_cost(self):
        """
        Calculate upgrade cost for slow duration based on slow duration level
        
        Returns:
            Dictionary of resource costs
        """
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with slow duration level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.slow_duration_level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def calculate_slow_duration_upgrade_monster_coin_cost(self):
        """
        Calculate Monster Coin cost for slow duration upgrade based on slow duration level
        
        Returns:
            Integer Monster Coin cost
        """
        base_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 15)  # Higher base for Frozen tower
        return int(base_cost * (TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER ** (self.slow_duration_level - 1)))
    
    def upgrade_slow_effect(self, resource_manager):
        """
        Upgrade tower slow effect
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        cost = self.calculate_slow_effect_upgrade_cost()
        monster_coin_cost = self.calculate_slow_effect_upgrade_monster_coin_cost()
        
        # Check if we have enough resources and Monster Coins
        if not resource_manager.has_resources(cost) or resource_manager.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        # Spend resources and Monster Coins
        if resource_manager and resource_manager.spend_resources(cost):
            # Spend the Monster Coins separately
            resource_manager.spend_resource("Monster Coins", monster_coin_cost)
            
            self.base_slow_effect = min(0.9, self.base_slow_effect * 1.2)
            self.slow_effect_level += 1
            self.level += 1  # Keep overall level for compatibility
            self.apply_item_effects()  # Re-apply item effects after upgrade
            return True
        return False
    
    def upgrade_slow_duration(self, resource_manager):
        """
        Upgrade tower slow duration
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        cost = self.calculate_slow_duration_upgrade_cost()
        monster_coin_cost = self.calculate_slow_duration_upgrade_monster_coin_cost()
        
        # Check if we have enough resources and Monster Coins
        if not resource_manager.has_resources(cost) or resource_manager.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        # Spend resources and Monster Coins
        if resource_manager and resource_manager.spend_resources(cost):
            # Spend the Monster Coins separately
            resource_manager.spend_resource("Monster Coins", monster_coin_cost)
            
            self.base_slow_duration *= 1.3
            self.slow_duration_level += 1
            self.level += 1  # Keep overall level for compatibility
            self.apply_item_effects()  # Re-apply item effects after upgrade
            return True
        return False
