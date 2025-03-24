# features/towers/factory.py
"""
Factory for tower creation in Castle Defense
"""
from .archer_tower import ArcherTower
from .sniper_tower import SniperTower
from .splash_tower import SplashTower
from .frozen_tower import FrozenTower

class TowerFactory:
    """Factory class for creating tower instances"""
    
    @staticmethod
    def create_tower(tower_type, position):
        """
        Create a tower of the specified type at the given position
        
        Args:
            tower_type: String indicating tower type
            position: Tuple of (x, y) coordinates
            
        Returns:
            Tower instance
            
        Raises:
            ValueError: If tower_type is invalid
        """
        if tower_type == "Archer":
            return ArcherTower(position)
        elif tower_type == "Sniper":
            return SniperTower(position)
        elif tower_type == "Splash":
            return SplashTower(position)
        elif tower_type == "Frozen":
            return FrozenTower(position)
        else:
            raise ValueError(f"Unknown tower type: {tower_type}")
