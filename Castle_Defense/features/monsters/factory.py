# features/monsters/factory.py
"""
Factory for monster creation in Castle Defense
"""
from .regular_monster import RegularMonster
from .boss_monster import BossMonster

class MonsterFactory:
    """Factory class for creating monster instances"""
    
    @staticmethod
    def create_regular_monster(monster_type, start_pos, target_pos, wave_number=1):
        """
        Create a regular monster of the specified type
        
        Args:
            monster_type: Type of monster (Grunt, Runner, Tank, Flyer)
            start_pos: Tuple of (x, y) starting coordinates
            target_pos: Tuple of (x, y) target coordinates (castle position)
            wave_number: Current wave number (for scaling difficulty)
            
        Returns:
            RegularMonster instance
        """
        return RegularMonster(start_pos, target_pos, monster_type, wave_number)
    
    @staticmethod
    def create_boss_monster(boss_type, start_pos, target_pos):
        """
        Create a boss monster of the specified type
        
        Args:
            boss_type: Type of boss (Force, Spirit, Magic, Void)
            start_pos: Tuple of (x, y) starting coordinates
            target_pos: Tuple of (x, y) target coordinates (castle position)
            
        Returns:
            BossMonster instance
        """
        return BossMonster(start_pos, target_pos, boss_type)
