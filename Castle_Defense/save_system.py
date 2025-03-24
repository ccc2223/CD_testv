# save_system.py
"""
Save system for Castle Defense game
"""
import os
import pickle
import datetime
from features.building_factory import BuildingFactory
from features.towers.factory import TowerFactory

class SaveManager:
    """Manages game saving and loading"""
    def __init__(self, game):
        """
        Initialize save manager
        
        Args:
            game: Game instance to save/load
        """
        self.game = game
        self.save_directory = "saves"
        self.max_saves = 10
        self.autosave_waves = 10
        
        # Create save directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def save_game(self, filename=None):
        """
        Save the current game state
        
        Args:
            filename: Optional filename, auto-generated if None
            
        Returns:
            Filename of saved game
        """
        # Generate filename if not provided
        if filename is None:
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
            wave_str = str(self.game.wave_manager.current_wave).zfill(3)
            filename = f"{date_str}-Wave{wave_str}.save"
        
        # Create serializable game state
        game_state = {
            "wave": self.game.wave_manager.current_wave,
            "resources": self.game.resource_manager.resources,
            "castle": {
                "health": self.game.castle.health,
                "max_health": self.game.castle.max_health,
                "damage_reduction": self.game.castle.damage_reduction,
                "health_regen": self.game.castle.health_regen,
                "level": self.game.castle.level
            },
            "buildings": [self.serialize_building(b) for b in self.game.buildings],
            "towers": [self.serialize_tower(t) for t in self.game.towers]
        }
        
        # Save to file
        filepath = os.path.join(self.save_directory, filename)
        with open(filepath, "wb") as f:
            pickle.dump(game_state, f)
        
        # Clean up old saves
        self.clean_old_saves()
        
        return filename
    
    def load_game(self, filename):
        """
        Load a saved game
        
        Args:
            filename: Filename to load
            
        Returns:
            True if load successful, False otherwise
        """
        filepath = os.path.join(self.save_directory, filename)
        if not os.path.exists(filepath):
            return False
        
        try:
            # Load game state
            with open(filepath, "rb") as f:
                game_state = pickle.load(f)
            
            # Restore wave
            self.game.wave_manager.current_wave = game_state["wave"]
            self.game.wave_manager.active_monsters = []
            self.game.wave_manager.wave_active = False
            self.game.wave_manager.wave_completed = True
            
            # Restore resources
            self.game.resource_manager.resources = game_state["resources"]
            
            # Restore castle
            castle_state = game_state["castle"]
            self.game.castle.health = castle_state["health"]
            self.game.castle.max_health = castle_state["max_health"]
            self.game.castle.damage_reduction = castle_state["damage_reduction"]
            self.game.castle.health_regen = castle_state["health_regen"]
            self.game.castle.level = castle_state["level"]
            
            # Restore buildings
            self.game.buildings = [self.deserialize_building(b) for b in game_state["buildings"]]
            
            # Restore towers
            self.game.towers = [self.deserialize_tower(t) for t in game_state["towers"]]
            
            return True
        
        except (pickle.PickleError, KeyError, AttributeError) as e:
            print(f"Error loading save: {e}")
            return False
    
    def check_autosave(self):
        """Check if we should autosave the game"""
        current_wave = self.game.wave_manager.current_wave
        if current_wave > 0 and current_wave % self.autosave_waves == 0 and self.game.wave_manager.wave_completed:
            self.save_game()
    
    def clean_old_saves(self):
        """Remove oldest save files if we have too many"""
        save_files = [f for f in os.listdir(self.save_directory) if f.endswith(".save")]
        save_files.sort()  # Sort by name, which includes date
        
        # Remove oldest files if we have too many
        if len(save_files) > self.max_saves:
            for i in range(0, len(save_files) - self.max_saves):
                os.remove(os.path.join(self.save_directory, save_files[i]))
    
    def serialize_building(self, building):
        """
        Create serializable representation of building
        
        Args:
            building: Building instance
            
        Returns:
            Dictionary of building data
        """
        building_data = {
            "type": building.__class__.__name__,
            "position": building.position,
            "level": building.level
        }
        
        # Add type-specific data
        if building.__class__.__name__ == "Mine":
            building_data.update({
                "resource_type": building.resource_type,
                "production_rate": building.production_rate,
                "production_timer": building.production_timer,
                "upgrade_timer": building.upgrade_timer,
                "upgrading": building.upgrading,
                "upgrade_time": building.upgrade_time
            })
        
        # Add Coresmith-specific data
        elif building.__class__.__name__ == "Coresmith":
            building_data.update({
                "crafting": building.crafting,
                "crafting_timer": building.crafting_timer,
                "crafting_time": building.crafting_time,
                "current_item": building.current_item
            })
        
        return building_data
    
    def deserialize_building(self, building_data):
        """
        Recreate building from serialized data
        
        Args:
            building_data: Dictionary of building data
            
        Returns:
            Building instance
        """
        building_type = building_data["type"]
        position = building_data["position"]
        
        try:
            building = BuildingFactory.create_building(building_type, position)
            
            # Set common properties
            building.level = building_data["level"]
            
            # Set building-specific properties
            if building_type == "Mine":
                building.resource_type = building_data["resource_type"]
                building.production_rate = building_data["production_rate"]
                building.production_timer = building_data["production_timer"]
                building.upgrade_timer = building_data["upgrade_timer"]
                building.upgrading = building_data["upgrading"]
                building.upgrade_time = building_data["upgrade_time"]
                building.update_resource_type()  # Update color based on resource type
            
            elif building_type == "Coresmith":
                building.crafting = building_data["crafting"]
                building.crafting_timer = building_data["crafting_timer"]
                building.crafting_time = building_data["crafting_time"]
                building.current_item = building_data["current_item"]
                
            return building
            
        except ValueError:
            # Fallback for unknown building types
            return BuildingFactory.create_building("Mine", position)
    
    def serialize_tower(self, tower):
        """
        Create serializable representation of tower
        
        Args:
            tower: Tower instance
            
        Returns:
            Dictionary of tower data
        """
        tower_data = {
            "type": tower.__class__.__name__,
            "position": tower.position,
            "level": tower.level,
            "damage": tower.damage,
            "attack_speed": tower.attack_speed,
            "range": tower.range,
            "item_slots": tower.item_slots
        }
        
        # Add tower-specific data
        if tower.__class__.__name__ == "SplashTower":
            tower_data["aoe_radius"] = tower.aoe_radius
        
        elif tower.__class__.__name__ == "FrozenTower":
            tower_data["slow_effect"] = tower.slow_effect
            tower_data["slow_duration"] = tower.slow_duration
        
        return tower_data
    
    def deserialize_tower(self, tower_data):
        """
        Recreate tower from serialized data
        
        Args:
            tower_data: Dictionary of tower data
            
        Returns:
            Tower instance
        """
        tower_type = tower_data["type"]
        position = tower_data["position"]
        
        try:
            tower = TowerFactory.create_tower(tower_type, position)
            
            # Set common properties
            tower.level = tower_data["level"]
            tower.damage = tower_data["damage"]
            tower.attack_speed = tower_data["attack_speed"]
            tower.range = tower_data["range"]
            tower.item_slots = tower_data["item_slots"]
            
            # Set tower-specific properties
            if tower_type == "SplashTower" and hasattr(tower, 'aoe_radius'):
                tower.aoe_radius = tower_data["aoe_radius"]
            
            elif tower_type == "FrozenTower" and hasattr(tower, 'slow_effect'):
                tower.slow_effect = tower_data["slow_effect"]
                tower.slow_duration = tower_data["slow_duration"]
            
            return tower
            
        except ValueError:
            # Fallback for unknown tower types
            return TowerFactory.create_tower("Archer", position)
