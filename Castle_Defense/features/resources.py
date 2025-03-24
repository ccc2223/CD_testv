# features/resources.py
"""
Resource management for the Castle Defense game
"""
from config import INITIAL_RESOURCES

class ResourceManager:
    """
    Manages game resources (Stone, Iron, Copper, Thorium, Monster Coins, etc.)
    """
    def __init__(self):
        """Initialize with default resource amounts"""
        self.resources = INITIAL_RESOURCES.copy()
    
    def add_resource(self, resource_type, amount):
        """
        Add resources of a specific type
        
        Args:
            resource_type: String name of resource
            amount: Amount to add
            
        Returns:
            True if resource was added, False if resource type is invalid
        """
        if resource_type in self.resources:
            self.resources[resource_type] += amount
            return True
        return False
    
    def spend_resource(self, resource_type, amount):
        """
        Spend resources of a specific type
        
        Args:
            resource_type: String name of resource
            amount: Amount to spend
            
        Returns:
            True if resources were spent, False if insufficient or invalid type
        """
        if resource_type in self.resources and self.resources[resource_type] >= amount:
            self.resources[resource_type] -= amount
            return True
        return False
    
    def spend_resources(self, cost_dict):
        """
        Spend multiple resource types according to a cost dictionary
        
        Args:
            cost_dict: Dictionary mapping resource types to amounts
            
        Returns:
            True if all resources were spent, False if insufficient
        """
        # First check if we have enough of all resources
        for resource_type, amount in cost_dict.items():
            if resource_type not in self.resources or self.resources[resource_type] < amount:
                return False
        
        # If we have enough, spend them
        for resource_type, amount in cost_dict.items():
            self.resources[resource_type] -= amount
        
        return True
    
    def has_resources(self, cost_dict):
        """
        Check if we have enough of all specified resources
        
        Args:
            cost_dict: Dictionary mapping resource types to amounts
            
        Returns:
            True if we have enough of all resources, False otherwise
        """
        for resource_type, amount in cost_dict.items():
            if resource_type not in self.resources or self.resources[resource_type] < amount:
                return False
        return True
    
    def get_resource(self, resource_type):
        """
        Get the current amount of a specific resource
        
        Args:
            resource_type: String name of resource
            
        Returns:
            Current amount of resource, or 0 if resource type is invalid
        """
        return self.resources.get(resource_type, 0)
    
    def has_resources_for_tower(self, resource_cost, monster_coin_cost):
        """
        Check if player has enough resources and Monster Coins for a tower
        
        Args:
            resource_cost: Dictionary mapping resource types to amounts
            monster_coin_cost: Amount of Monster Coins required
            
        Returns:
            True if player has enough of all required resources, False otherwise
        """
        # Check regular resources
        if not self.has_resources(resource_cost):
            return False
        
        # Check Monster Coins
        if self.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        return True
    
    def spend_resources_for_tower(self, resource_cost, monster_coin_cost):
        """
        Spend resources and Monster Coins for tower placement or upgrade
        
        Args:
            resource_cost: Dictionary mapping resource types to amounts
            monster_coin_cost: Amount of Monster Coins to spend
            
        Returns:
            True if resources were successfully spent, False otherwise
        """
        # First check if we have enough of everything
        if not self.has_resources_for_tower(resource_cost, monster_coin_cost):
            return False
        
        # Spend regular resources
        for resource_type, amount in resource_cost.items():
            self.resources[resource_type] -= amount
        
        # Spend Monster Coins
        self.resources["Monster Coins"] -= monster_coin_cost
        
        return True
