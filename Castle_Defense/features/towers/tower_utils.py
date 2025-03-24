# towers/tower_utils.py
"""
Utility functions for tower operations
"""

def calculate_upgrade_cost(base_cost, multiplier, level):
    """
    Calculate the upgrade cost based on level
    
    Args:
        base_cost: Dictionary of base costs
        multiplier: Cost multiplier per level
        level: Current level
        
    Returns:
        Dictionary of scaled costs
    """
    return {
        resource_type: int(amount * (multiplier ** (level - 1)))
        for resource_type, amount in base_cost.items()
    }

def calculate_monster_coin_cost(base_cost, multiplier, level):
    """
    Calculate Monster Coin cost for upgrades
    
    Args:
        base_cost: Base Monster Coin cost
        multiplier: Cost multiplier per level
        level: Current level
        
    Returns:
        Integer Monster Coin cost
    """
    return int(base_cost * (multiplier ** (level - 1)))

def get_target_by_strategy(strategy, monsters):
    """
    Get a target based on targeting strategy
    
    Args:
        strategy: String naming the targeting strategy
        monsters: List of monsters to select from
        
    Returns:
        Selected monster or None if no valid targets
    """
    if not monsters:
        return None
        
    if strategy == "nearest":
        return monsters[0]  # Monsters are already sorted by distance
    elif strategy == "furthest":
        return monsters[-1]
    elif strategy == "highest_health":
        return max(monsters, key=lambda m: m.health)
    elif strategy == "lowest_health":
        return min(monsters, key=lambda m: m.health)
    else:
        # Default to nearest
        return monsters[0]

def handle_item_effects(tower, item_effects):
    """
    Apply item effects to tower stats
    
    Args:
        tower: Tower instance
        item_effects: Dictionary of effect configurations
        
    Returns:
        Updated tower stats dictionary
    """
    stats = {
        "damage": tower.damage,
        "attack_speed": tower.attack_speed,
        "range": tower.range,
        "splash_enabled": False,
        "splash_radius": 0,
        "healing_enabled": False,
        "healing_percentage": 0
    }
    
    # Apply specific item effects
    for item in tower.item_slots:
        if item == "Unstoppable Force":
            # Apply AoE effects
            if tower.tower_type in ["Splash", "Frozen"]:
                # These towers already have AoE, so enhance it
                if tower.tower_type == "Splash":
                    stats["aoe_radius"] = tower.aoe_radius * 1.3
                else:
                    stats["range"] *= 1.3
            else:
                # Add splash damage to single-target towers
                stats["splash_enabled"] = True
                stats["splash_radius"] = 30  # Base splash radius
        
        elif item == "Serene Spirit":
            # Enable healing based on damage
            stats["healing_enabled"] = True
            stats["healing_percentage"] = 0.05  # 5% of damage converted to healing
    
    return stats
