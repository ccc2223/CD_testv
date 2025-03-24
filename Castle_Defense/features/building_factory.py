# features/building_factory.py
"""
Factory for building creation in Castle Defense
"""
from .buildings import Mine, Coresmith, CastleUpgradeStation

class BuildingFactory:
    """Factory class for creating building instances"""
    
    @staticmethod
    def create_building(building_type, position):
        """
        Create a building of the specified type at the given position
        
        Args:
            building_type: String indicating building type
            position: Tuple of (x, y) coordinates
            
        Returns:
            Building instance
            
        Raises:
            ValueError: If building_type is invalid
        """
        if building_type == "Mine":
            return Mine(position)
        elif building_type == "Coresmith":
            return Coresmith(position)
        elif building_type == "CastleUpgradeStation":
            return CastleUpgradeStation(position)
        else:
            raise ValueError(f"Unknown building type: {building_type}")
