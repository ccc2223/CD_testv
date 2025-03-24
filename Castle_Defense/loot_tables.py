# loot_tables.py
"""
Loot table system for Castle Defense
"""
import random
import math

class LootTable:
    """
    Defines a loot table with weighted items, min/max quantities, and wave-based scaling
    """
    def __init__(self, entries=None):
        """
        Initialize a loot table with entries
        
        Args:
            entries: List of LootEntry objects (optional)
        """
        self.entries = entries or []
    
    def add_entry(self, entry):
        """
        Add a loot entry to the table
        
        Args:
            entry: LootEntry to add
        """
        self.entries.append(entry)
    
    def get_loot(self, wave=1):
        """
        Generate loot from this table
        
        Args:
            wave: Current wave number for scaling (default: 1)
            
        Returns:
            Dictionary of {resource_type: amount} for all dropped items
        """
        result = {}
        
        for entry in self.entries:
            # Check if this entry should drop
            if random.random() <= entry.get_drop_chance(wave):
                # Determine the drop quantity
                quantity = entry.get_quantity(wave)
                
                if quantity > 0:
                    # Add to results
                    resource_type = entry.resource_type
                    if resource_type in result:
                        result[resource_type] += quantity
                    else:
                        result[resource_type] = quantity
        
        return result

class LootEntry:
    """
    Represents a single item in a loot table with drop chance and quantity settings
    """
    def __init__(self, resource_type, base_chance=1.0, min_quantity=1, max_quantity=1, 
                 chance_scaling=0.0, quantity_scaling=0.0):
        """
        Initialize a loot entry
        
        Args:
            resource_type: String resource type to drop
            base_chance: Base chance to drop (0.0 to 1.0)
            min_quantity: Minimum quantity to drop
            max_quantity: Maximum quantity to drop
            chance_scaling: How much drop chance increases per wave
            quantity_scaling: How much quantity increases per wave
        """
        self.resource_type = resource_type
        self.base_chance = base_chance
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.chance_scaling = chance_scaling
        self.quantity_scaling = quantity_scaling
    
    def get_drop_chance(self, wave):
        """
        Calculate the actual drop chance based on wave number
        
        Args:
            wave: Current wave number
            
        Returns:
            Final drop chance (0.0 to 1.0)
        """
        # Apply wave scaling to drop chance
        chance = self.base_chance + (wave - 1) * self.chance_scaling
        
        # Clamp between 0 and 1
        return max(0.0, min(1.0, chance))
    
    def get_quantity(self, wave):
        """
        Calculate the quantity to drop based on wave number
        
        Args:
            wave: Current wave number
            
        Returns:
            Integer quantity to drop
        """
        # Apply wave scaling to quantities
        min_qty = self.min_quantity + (wave - 1) * self.quantity_scaling
        max_qty = self.max_quantity + (wave - 1) * self.quantity_scaling
        
        # Ensure max is at least min
        max_qty = max(min_qty, max_qty)
        
        # Get a random integer between min and max
        # Use math.floor to ensure we get correct integers when using floats
        min_qty_int = math.floor(min_qty)
        max_qty_int = math.floor(max_qty)
        
        if min_qty_int == max_qty_int:
            return min_qty_int
        else:
            return random.randint(min_qty_int, max_qty_int)

# Define loot tables for each monster type
def get_monster_loot_table(monster_type):
    """
    Get the loot table for a specific monster type
    
    Args:
        monster_type: String monster type
        
    Returns:
        LootTable for that monster type
    """
    loot_table = LootTable()
    
    if monster_type == "Grunt":
        # Basic guaranteed Monster Coin drop
        loot_table.add_entry(LootEntry(
            "Monster Coins", 
            base_chance=1.0, 
            min_quantity=1, 
            max_quantity=1,
            quantity_scaling=0.1  # Slowly increase over waves
        ))
        
        # Small chance for Stone
        loot_table.add_entry(LootEntry(
            "Stone", 
            base_chance=0.2, 
            min_quantity=1, 
            max_quantity=2,
            chance_scaling=0.01,
            quantity_scaling=0.05
        ))
    
    elif monster_type == "Runner":
        # Higher coins but less chance of resources
        loot_table.add_entry(LootEntry(
            "Monster Coins", 
            base_chance=1.0, 
            min_quantity=1, 
            max_quantity=2,
            quantity_scaling=0.1
        ))
        
        # Low chance for Iron after wave 5
        loot_table.add_entry(LootEntry(
            "Iron", 
            base_chance=0.0, 
            min_quantity=1, 
            max_quantity=1,
            chance_scaling=0.02  # Starts dropping at wave 5
        ))
    
    elif monster_type == "Tank":
        # Tanky monsters give more coins
        loot_table.add_entry(LootEntry(
            "Monster Coins", 
            base_chance=1.0, 
            min_quantity=2, 
            max_quantity=3,
            quantity_scaling=0.15
        ))
        
        # Better chance for Stone
        loot_table.add_entry(LootEntry(
            "Stone", 
            base_chance=0.4, 
            min_quantity=2, 
            max_quantity=4,
            chance_scaling=0.01,
            quantity_scaling=0.1
        ))
        
        # Chance for Iron
        loot_table.add_entry(LootEntry(
            "Iron", 
            base_chance=0.2, 
            min_quantity=1, 
            max_quantity=2,
            chance_scaling=0.02,
            quantity_scaling=0.05
        ))
    
    elif monster_type == "Flyer":
        # Fast fliers drop more coins but less resources
        loot_table.add_entry(LootEntry(
            "Monster Coins", 
            base_chance=1.0, 
            min_quantity=2, 
            max_quantity=2,
            quantity_scaling=0.1
        ))
        
        # Chance for Copper (rare resource)
        loot_table.add_entry(LootEntry(
            "Copper", 
            base_chance=0.1, 
            min_quantity=1, 
            max_quantity=1,
            chance_scaling=0.01
        ))
    
    else:
        # Default loot table for unknown monster types
        loot_table.add_entry(LootEntry("Monster Coins", 1.0, 1, 1))
    
    return loot_table

# Define boss loot tables
def get_boss_loot_table(boss_type, wave):
    """
    Get the loot table for a specific boss type
    
    Args:
        boss_type: String boss type
        wave: Current wave number
        
    Returns:
        LootTable for that boss type
    """
    loot_table = LootTable()
    
    # All bosses drop Monster Coins
    loot_table.add_entry(LootEntry(
        "Monster Coins", 
        base_chance=1.0, 
        min_quantity=8, 
        max_quantity=12,
        quantity_scaling=0.5  # Bosses give more coins in later waves
    ))
    
    # Core drops based on boss type (guaranteed)
    core_type = f"{boss_type} Core"
    loot_table.add_entry(LootEntry(
        core_type, 
        base_chance=1.0, 
        min_quantity=1, 
        max_quantity=math.ceil(wave / 30) + 1  # More cores in much later waves
    ))
    
    # Additional drops based on boss type
    if boss_type == "Force":
        # Force bosses drop more Stone
        loot_table.add_entry(LootEntry(
            "Stone", 
            base_chance=1.0, 
            min_quantity=10, 
            max_quantity=15,
            quantity_scaling=0.2
        ))
        
    elif boss_type == "Spirit":
        # Spirit bosses drop Iron
        loot_table.add_entry(LootEntry(
            "Iron", 
            base_chance=1.0, 
            min_quantity=5, 
            max_quantity=8,
            quantity_scaling=0.15
        ))
        
    elif boss_type == "Magic":
        # Magic bosses drop Copper
        loot_table.add_entry(LootEntry(
            "Copper", 
            base_chance=1.0, 
            min_quantity=3, 
            max_quantity=5,
            quantity_scaling=0.1
        ))
        
    elif boss_type == "Void":
        # Void bosses are the most powerful and drop Thorium
        loot_table.add_entry(LootEntry(
            "Thorium", 
            base_chance=1.0, 
            min_quantity=1, 
            max_quantity=3,
            quantity_scaling=0.05
        ))
        
        # Void bosses also have a small chance to drop other cores
        other_cores = ["Force Core", "Spirit Core", "Magic Core"]
        for core in other_cores:
            if core != core_type:  # Don't double-drop the boss's own core
                loot_table.add_entry(LootEntry(
                    core, 
                    base_chance=0.2, 
                    min_quantity=1, 
                    max_quantity=1
                ))
    
    return loot_table
