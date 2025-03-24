# monsters/regular_monster.py
"""
Regular monster implementation for Castle Defense
"""
from .base_monster import Monster
from config import MONSTER_STATS

class RegularMonster(Monster):
    """Implementation of regular monster types (Grunt, Runner, Tank, Flyer)"""
    def __init__(self, start_pos, target_pos, monster_type, wave_number=1):
        """
        Initialize regular monster
        
        Args:
            start_pos: Tuple of (x, y) starting coordinates
            target_pos: Tuple of (x, y) target coordinates (castle position)
            monster_type: Type of monster (Grunt, Runner, Tank, Flyer)
            wave_number: Current wave number (for scaling difficulty)
        """
        # Get base stats from config
        stats = MONSTER_STATS.get(monster_type, {}).copy()
        
        # Scale stats based on wave number
        if wave_number > 1:
            # Apply wave difficulty multiplier (based on how it's defined in your config)
            from config import WAVE_DIFFICULTY_MULTIPLIER
            difficulty_multiplier = WAVE_DIFFICULTY_MULTIPLIER ** (wave_number // 5)
            stats["health"] = int(stats["health"] * difficulty_multiplier)
            stats["damage"] = int(stats["damage"] * difficulty_multiplier)
        
        # Initialize with the base Monster class
        super().__init__(start_pos, target_pos, monster_type, stats)
        
        # Store wave number for reference
        self.wave_number = wave_number
        
        # Specific behavior flags based on monster type
        if monster_type == "Runner":
            self.attack_interval = 0.8  # Faster attacks
        elif monster_type == "Tank":
            self.attack_interval = 1.5  # Slower but harder hits
        elif monster_type == "Flyer":
            self.flying = True  # Make sure flying flag is set
