# config_extension.py
"""
Extended configuration support for dynamic parameter adjustments
"""
import copy
import importlib
import sys

# Import original config values
from config import (
    WAVE_DIFFICULTY_MULTIPLIER, MONSTER_SPAWN_INTERVAL,
    WAVE_MONSTER_COUNT_BASE, WAVE_MONSTER_COUNT_MULTIPLIER,
    MONSTER_STATS, BOSS_STATS,
    MINE_INITIAL_PRODUCTION, MINE_PRODUCTION_MULTIPLIER,
    LOOT_MONSTER_BASE_COIN_DROP, LOOT_BOSS_BASE_COIN_DROP, LOOT_WAVE_SCALING,
    ITEM_COSTS, ITEM_EFFECTS,
    TOWER_TYPES, TOWER_UPGRADE_COST_MULTIPLIER, TOWER_MONSTER_COIN_COSTS, TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
    TOWER_DAMAGE_UPGRADE_MULTIPLIER, TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER, TOWER_RANGE_UPGRADE_MULTIPLIER,
    CASTLE_HEALTH_UPGRADE_COST, CASTLE_DAMAGE_REDUCTION_UPGRADE_COST, CASTLE_HEALTH_REGEN_UPGRADE_COST,
    CASTLE_HEALTH_UPGRADE_MULTIPLIER, CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER, CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
)

# Store original values for reset functionality
ORIGINAL_VALUES = {
    "WAVE_DIFFICULTY_MULTIPLIER": WAVE_DIFFICULTY_MULTIPLIER,
    "MONSTER_SPAWN_INTERVAL": MONSTER_SPAWN_INTERVAL,
    "WAVE_MONSTER_COUNT_BASE": WAVE_MONSTER_COUNT_BASE,
    "WAVE_MONSTER_COUNT_MULTIPLIER": WAVE_MONSTER_COUNT_MULTIPLIER,
    "MONSTER_STATS": copy.deepcopy(MONSTER_STATS),
    "BOSS_STATS": copy.deepcopy(BOSS_STATS),
    "MINE_INITIAL_PRODUCTION": MINE_INITIAL_PRODUCTION,
    "MINE_PRODUCTION_MULTIPLIER": MINE_PRODUCTION_MULTIPLIER,
    "LOOT_MONSTER_BASE_COIN_DROP": LOOT_MONSTER_BASE_COIN_DROP,
    "LOOT_BOSS_BASE_COIN_DROP": LOOT_BOSS_BASE_COIN_DROP,
    "LOOT_WAVE_SCALING": LOOT_WAVE_SCALING,
    "ITEM_COSTS": copy.deepcopy(ITEM_COSTS),
    "ITEM_EFFECTS": copy.deepcopy(ITEM_EFFECTS),
    "TOWER_TYPES": copy.deepcopy(TOWER_TYPES),
    "TOWER_UPGRADE_COST_MULTIPLIER": TOWER_UPGRADE_COST_MULTIPLIER,
    "TOWER_MONSTER_COIN_COSTS": copy.deepcopy(TOWER_MONSTER_COIN_COSTS),
    "TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER": TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
    "TOWER_DAMAGE_UPGRADE_MULTIPLIER": TOWER_DAMAGE_UPGRADE_MULTIPLIER,
    "TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER": TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER,
    "TOWER_RANGE_UPGRADE_MULTIPLIER": TOWER_RANGE_UPGRADE_MULTIPLIER,
    "CASTLE_HEALTH_UPGRADE_COST": copy.deepcopy(CASTLE_HEALTH_UPGRADE_COST),
    "CASTLE_DAMAGE_REDUCTION_UPGRADE_COST": copy.deepcopy(CASTLE_DAMAGE_REDUCTION_UPGRADE_COST),
    "CASTLE_HEALTH_REGEN_UPGRADE_COST": copy.deepcopy(CASTLE_HEALTH_REGEN_UPGRADE_COST),
    "CASTLE_HEALTH_UPGRADE_MULTIPLIER": CASTLE_HEALTH_UPGRADE_MULTIPLIER,
    "CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER": CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER,
    "CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER": CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
}

# Dynamic configuration functions

# Monster balance functions
def set_wave_difficulty_multiplier(value):
    """Set the wave difficulty multiplier"""
    module = sys.modules['config']
    module.WAVE_DIFFICULTY_MULTIPLIER = value

def set_monster_spawn_interval(value):
    """Set the monster spawn interval"""
    module = sys.modules['config']
    module.MONSTER_SPAWN_INTERVAL = value

def set_wave_monster_count_base(value):
    """Set the base number of monsters per wave"""
    module = sys.modules['config']
    module.WAVE_MONSTER_COUNT_BASE = value

def set_wave_monster_count_multiplier(value):
    """Set the wave monster count multiplier"""
    module = sys.modules['config']
    module.WAVE_MONSTER_COUNT_MULTIPLIER = value

def update_monster_stats(monster_type, stat, value):
    """Update a specific stat for a monster type"""
    if monster_type in MONSTER_STATS and stat in MONSTER_STATS[monster_type]:
        module = sys.modules['config']
        module.MONSTER_STATS[monster_type][stat] = value

def update_monster_stats_all(monster_type, stats_dict):
    """Update all stats for a monster type"""
    if monster_type in MONSTER_STATS:
        module = sys.modules['config']
        module.MONSTER_STATS[monster_type] = copy.deepcopy(stats_dict)

def update_boss_stats(boss_type, stat, value):
    """Update a specific stat for a boss type"""
    if boss_type in BOSS_STATS and stat in BOSS_STATS[boss_type]:
        module = sys.modules['config']
        module.BOSS_STATS[boss_type][stat] = value

def update_boss_stats_all(boss_type, stats_dict):
    """Update all stats for a boss type"""
    if boss_type in BOSS_STATS:
        module = sys.modules['config']
        module.BOSS_STATS[boss_type] = copy.deepcopy(stats_dict)

# Economy functions
def set_mine_initial_production(value):
    """Set the initial mine production rate"""
    module = sys.modules['config']
    module.MINE_INITIAL_PRODUCTION = value

def set_mine_production_multiplier(value):
    """Set the mine production multiplier"""
    module = sys.modules['config']
    module.MINE_PRODUCTION_MULTIPLIER = value

def set_loot_monster_base_coin_drop(value):
    """Set the base monster coin drop"""
    module = sys.modules['config']
    module.LOOT_MONSTER_BASE_COIN_DROP = value

def set_loot_boss_base_coin_drop(value):
    """Set the base boss coin drop"""
    module = sys.modules['config']
    module.LOOT_BOSS_BASE_COIN_DROP = value
    # Update the backward compatibility constant
    module.BOSS_COIN_DROP = value

def set_loot_wave_scaling(value):
    """Set the loot wave scaling factor"""
    module = sys.modules['config']
    module.LOOT_WAVE_SCALING = value

def update_item_cost(item_name, resource, value):
    """Update the cost of an item"""
    if item_name in ITEM_COSTS:
        module = sys.modules['config']
        module.ITEM_COSTS[item_name][resource] = value

def update_castle_upgrade_cost(upgrade_type, resource, value):
    """Update castle upgrade cost"""
    module = sys.modules['config']
    
    if upgrade_type == "health":
        module.CASTLE_HEALTH_UPGRADE_COST[resource] = value
    elif upgrade_type == "damage_reduction":
        module.CASTLE_DAMAGE_REDUCTION_UPGRADE_COST[resource] = value
    elif upgrade_type == "health_regen":
        module.CASTLE_HEALTH_REGEN_UPGRADE_COST[resource] = value

def reset_castle_upgrade_costs():
    """Reset all castle upgrade costs to original values"""
    module = sys.modules['config']
    module.CASTLE_HEALTH_UPGRADE_COST = copy.deepcopy(ORIGINAL_VALUES["CASTLE_HEALTH_UPGRADE_COST"])
    module.CASTLE_DAMAGE_REDUCTION_UPGRADE_COST = copy.deepcopy(ORIGINAL_VALUES["CASTLE_DAMAGE_REDUCTION_UPGRADE_COST"])
    module.CASTLE_HEALTH_REGEN_UPGRADE_COST = copy.deepcopy(ORIGINAL_VALUES["CASTLE_HEALTH_REGEN_UPGRADE_COST"])

def set_castle_health_upgrade_multiplier(value):
    """Set castle health upgrade multiplier"""
    module = sys.modules['config']
    module.CASTLE_HEALTH_UPGRADE_MULTIPLIER = value

def set_castle_damage_reduction_upgrade_multiplier(value):
    """Set castle damage reduction upgrade multiplier"""
    module = sys.modules['config']
    module.CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER = value

def set_castle_health_regen_upgrade_multiplier(value):
    """Set castle health regen upgrade multiplier"""
    module = sys.modules['config']
    module.CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER = value

# Tower functions
def update_tower_stat(tower_type, stat, value):
    """Update a specific stat for a tower type"""
    if tower_type in TOWER_TYPES and stat in TOWER_TYPES[tower_type]:
        module = sys.modules['config']
        module.TOWER_TYPES[tower_type][stat] = value

def update_tower_cost(tower_type, resource, value):
    """Update tower resource cost"""
    if tower_type in TOWER_TYPES:
        module = sys.modules['config']
        
        # Ensure cost dictionary exists
        if "cost" not in module.TOWER_TYPES[tower_type]:
            module.TOWER_TYPES[tower_type]["cost"] = {}
        
        module.TOWER_TYPES[tower_type]["cost"][resource] = value

def update_tower_monster_coin_cost(tower_type, value):
    """Update tower Monster Coin cost"""
    if tower_type in TOWER_MONSTER_COIN_COSTS:
        module = sys.modules['config']
        module.TOWER_MONSTER_COIN_COSTS[tower_type] = value

def set_tower_upgrade_cost_multiplier(value):
    """Set tower upgrade cost multiplier"""
    module = sys.modules['config']
    module.TOWER_UPGRADE_COST_MULTIPLIER = value

def set_tower_monster_coin_upgrade_multiplier(value):
    """Set tower Monster Coin upgrade multiplier"""
    module = sys.modules['config']
    module.TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER = value

def set_tower_damage_upgrade_multiplier(value):
    """Set tower damage upgrade multiplier"""
    module = sys.modules['config']
    module.TOWER_DAMAGE_UPGRADE_MULTIPLIER = value

def set_tower_attack_speed_upgrade_multiplier(value):
    """Set tower attack speed upgrade multiplier"""
    module = sys.modules['config']
    module.TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER = value

def set_tower_range_upgrade_multiplier(value):
    """Set tower range upgrade multiplier"""
    module = sys.modules['config']
    module.TOWER_RANGE_UPGRADE_MULTIPLIER = value

# Configuration save/load functions
def get_all_config_values():
    """
    Get all configuration values as a dictionary
    
    Returns:
        Dictionary of all configuration values
    """
    module = sys.modules['config']
    
    # Build a dictionary of all configuration values
    config_values = {
        "WAVE_DIFFICULTY_MULTIPLIER": module.WAVE_DIFFICULTY_MULTIPLIER,
        "MONSTER_SPAWN_INTERVAL": module.MONSTER_SPAWN_INTERVAL,
        "WAVE_MONSTER_COUNT_BASE": module.WAVE_MONSTER_COUNT_BASE,
        "WAVE_MONSTER_COUNT_MULTIPLIER": module.WAVE_MONSTER_COUNT_MULTIPLIER,
        "MONSTER_STATS": copy.deepcopy(module.MONSTER_STATS),
        "BOSS_STATS": copy.deepcopy(module.BOSS_STATS),
        "MINE_INITIAL_PRODUCTION": module.MINE_INITIAL_PRODUCTION,
        "MINE_PRODUCTION_MULTIPLIER": module.MINE_PRODUCTION_MULTIPLIER,
        "LOOT_MONSTER_BASE_COIN_DROP": module.LOOT_MONSTER_BASE_COIN_DROP,
        "LOOT_BOSS_BASE_COIN_DROP": module.LOOT_BOSS_BASE_COIN_DROP,
        "LOOT_WAVE_SCALING": module.LOOT_WAVE_SCALING,
        "ITEM_COSTS": copy.deepcopy(module.ITEM_COSTS),
        "TOWER_TYPES": copy.deepcopy(module.TOWER_TYPES),
        "TOWER_MONSTER_COIN_COSTS": copy.deepcopy(module.TOWER_MONSTER_COIN_COSTS),
        "TOWER_UPGRADE_COST_MULTIPLIER": module.TOWER_UPGRADE_COST_MULTIPLIER,
        "TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER": module.TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
        "TOWER_DAMAGE_UPGRADE_MULTIPLIER": module.TOWER_DAMAGE_UPGRADE_MULTIPLIER,
        "TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER": module.TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER,
        "TOWER_RANGE_UPGRADE_MULTIPLIER": module.TOWER_RANGE_UPGRADE_MULTIPLIER,
        "CASTLE_HEALTH_UPGRADE_COST": copy.deepcopy(module.CASTLE_HEALTH_UPGRADE_COST),
        "CASTLE_DAMAGE_REDUCTION_UPGRADE_COST": copy.deepcopy(module.CASTLE_DAMAGE_REDUCTION_UPGRADE_COST),
        "CASTLE_HEALTH_REGEN_UPGRADE_COST": copy.deepcopy(module.CASTLE_HEALTH_REGEN_UPGRADE_COST),
        "CASTLE_HEALTH_UPGRADE_MULTIPLIER": module.CASTLE_HEALTH_UPGRADE_MULTIPLIER,
        "CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER": module.CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER,
        "CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER": module.CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER
    }
    
    return config_values

def apply_all_config_values(config_dict):
    """
    Apply all configuration values from a dictionary
    
    Args:
        config_dict: Dictionary of configuration values
    """
    # Apply monster balance settings
    if "WAVE_DIFFICULTY_MULTIPLIER" in config_dict:
        set_wave_difficulty_multiplier(config_dict["WAVE_DIFFICULTY_MULTIPLIER"])
    if "MONSTER_SPAWN_INTERVAL" in config_dict:
        set_monster_spawn_interval(config_dict["MONSTER_SPAWN_INTERVAL"])
    if "WAVE_MONSTER_COUNT_BASE" in config_dict:
        set_wave_monster_count_base(config_dict["WAVE_MONSTER_COUNT_BASE"])
    if "WAVE_MONSTER_COUNT_MULTIPLIER" in config_dict:
        set_wave_monster_count_multiplier(config_dict["WAVE_MONSTER_COUNT_MULTIPLIER"])
    
    # Apply monster stats
    if "MONSTER_STATS" in config_dict:
        for monster_type, stats in config_dict["MONSTER_STATS"].items():
            update_monster_stats_all(monster_type, stats)
    
    # Apply boss stats
    if "BOSS_STATS" in config_dict:
        for boss_type, stats in config_dict["BOSS_STATS"].items():
            update_boss_stats_all(boss_type, stats)
    
    # Apply economy settings
    if "MINE_INITIAL_PRODUCTION" in config_dict:
        set_mine_initial_production(config_dict["MINE_INITIAL_PRODUCTION"])
    if "MINE_PRODUCTION_MULTIPLIER" in config_dict:
        set_mine_production_multiplier(config_dict["MINE_PRODUCTION_MULTIPLIER"])
    if "LOOT_MONSTER_BASE_COIN_DROP" in config_dict:
        set_loot_monster_base_coin_drop(config_dict["LOOT_MONSTER_BASE_COIN_DROP"])
    if "LOOT_BOSS_BASE_COIN_DROP" in config_dict:
        set_loot_boss_base_coin_drop(config_dict["LOOT_BOSS_BASE_COIN_DROP"])
    if "LOOT_WAVE_SCALING" in config_dict:
        set_loot_wave_scaling(config_dict["LOOT_WAVE_SCALING"])
    
    # Apply item costs
    if "ITEM_COSTS" in config_dict:
        for item_name, costs in config_dict["ITEM_COSTS"].items():
            for resource, amount in costs.items():
                update_item_cost(item_name, resource, amount)
    
    # Apply tower settings
    if "TOWER_TYPES" in config_dict:
        for tower_type, data in config_dict["TOWER_TYPES"].items():
            # Apply base stats
            for stat, value in data.items():
                if stat != "cost":
                    update_tower_stat(tower_type, stat, value)
            
            # Apply costs
            if "cost" in data:
                for resource, amount in data["cost"].items():
                    update_tower_cost(tower_type, resource, amount)
    
    # Apply Monster Coin costs for towers
    if "TOWER_MONSTER_COIN_COSTS" in config_dict:
        for tower_type, amount in config_dict["TOWER_MONSTER_COIN_COSTS"].items():
            update_tower_monster_coin_cost(tower_type, amount)
    
    # Apply tower upgrade settings
    if "TOWER_UPGRADE_COST_MULTIPLIER" in config_dict:
        set_tower_upgrade_cost_multiplier(config_dict["TOWER_UPGRADE_COST_MULTIPLIER"])
    if "TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER" in config_dict:
        set_tower_monster_coin_upgrade_multiplier(config_dict["TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER"])
    if "TOWER_DAMAGE_UPGRADE_MULTIPLIER" in config_dict:
        set_tower_damage_upgrade_multiplier(config_dict["TOWER_DAMAGE_UPGRADE_MULTIPLIER"])
    if "TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER" in config_dict:
        set_tower_attack_speed_upgrade_multiplier(config_dict["TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER"])
    if "TOWER_RANGE_UPGRADE_MULTIPLIER" in config_dict:
        set_tower_range_upgrade_multiplier(config_dict["TOWER_RANGE_UPGRADE_MULTIPLIER"])
    
    # Apply castle upgrade settings
    if "CASTLE_HEALTH_UPGRADE_COST" in config_dict:
        for resource, amount in config_dict["CASTLE_HEALTH_UPGRADE_COST"].items():
            update_castle_upgrade_cost("health", resource, amount)
    if "CASTLE_DAMAGE_REDUCTION_UPGRADE_COST" in config_dict:
        for resource, amount in config_dict["CASTLE_DAMAGE_REDUCTION_UPGRADE_COST"].items():
            update_castle_upgrade_cost("damage_reduction", resource, amount)
    if "CASTLE_HEALTH_REGEN_UPGRADE_COST" in config_dict:
        for resource, amount in config_dict["CASTLE_HEALTH_REGEN_UPGRADE_COST"].items():
            update_castle_upgrade_cost("health_regen", resource, amount)
    
    if "CASTLE_HEALTH_UPGRADE_MULTIPLIER" in config_dict:
        set_castle_health_upgrade_multiplier(config_dict["CASTLE_HEALTH_UPGRADE_MULTIPLIER"])
    if "CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER" in config_dict:
        set_castle_damage_reduction_upgrade_multiplier(config_dict["CASTLE_DAMAGE_REDUCTION_UPGRADE_MULTIPLIER"])
    if "CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER" in config_dict:
        set_castle_health_regen_upgrade_multiplier(config_dict["CASTLE_HEALTH_REGEN_UPGRADE_MULTIPLIER"])