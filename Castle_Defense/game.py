# game.py - Modified with main menu integration
import pygame
import sys
import math
from features.resources import ResourceManager
from features.castle import Castle
from features.building_factory import BuildingFactory
from features.waves import WaveManager
from features.towers.factory import TowerFactory
from ui.game_ui import GameUI, TowerPlacementUI
from ui.menus import BuildingMenu, TowerMenu
from ui.castle_menu import CastleMenu
from ui.dev_menu import DeveloperMenu
from save_system import SaveManager
from effects.animation_manager import AnimationManager
from config import FPS, BACKGROUND_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT, TOWER_TYPES, REF_WIDTH, REF_HEIGHT
from utils import distance, scale_position, scale_size, scale_value, unscale_position

# Import the state management system
from states import GameStateManager, PlayingState, PausedState, TowerPlacementState, GameOverState, MainMenuState

# Import config_extension to enable dynamic parameter updates
import config_extension

# Make the Game class globally accessible for tower attack callbacks
game_instance = None

class Game:
    """
    Main game class that manages the game state, updates, and rendering.
    """
    def __init__(self, screen):
        """
        Initialize the game with required components.
        
        Args:
            screen: Pygame surface for drawing
        """
        global game_instance
        game_instance = self
        
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game speed control (for developer menu)
        self.time_scale = 1.0
        
        # Save references to constants for easier use throughout the code
        self.BACKGROUND_COLOR = BACKGROUND_COLOR
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.TOWER_TYPES = TOWER_TYPES
        self.REF_WIDTH = REF_WIDTH
        self.REF_HEIGHT = REF_HEIGHT
        
        # Expose utility functions for use by state classes
        self.scale_position = scale_position
        self.scale_size = scale_size
        self.scale_value = scale_value
        self.unscale_position = unscale_position
        self.distance = distance
        
        # Initialize game components
        self.resource_manager = ResourceManager()
        self.castle = Castle()
        self.wave_manager = WaveManager()
        
        # Initialize buildings and towers
        self.buildings = []
        self.towers = []
        
        # Create the castle first so we can use its position
        # Position buildings below the castle (outside the castle walls)
        # Define positions in reference coordinates then scale
        ref_mine_pos = (self.castle.ref_position[0] - 100, 
                        self.castle.ref_position[1] + self.castle.ref_size[1] // 2 + 30)
        mine_pos = scale_position(ref_mine_pos)
        self.buildings.append(BuildingFactory.create_building("Mine", mine_pos))
        
        ref_coresmith_pos = (self.castle.ref_position[0] + 100, 
                             self.castle.ref_position[1] + self.castle.ref_size[1] // 2 + 30)
        coresmith_pos = scale_position(ref_coresmith_pos)
        self.buildings.append(BuildingFactory.create_building("Coresmith", coresmith_pos))
        
        # Add Castle Upgrade Station to the right of Coresmith
        ref_upgrade_station_pos = (ref_coresmith_pos[0] + 100, ref_coresmith_pos[1])
        upgrade_station_pos = scale_position(ref_upgrade_station_pos)
        self.buildings.append(BuildingFactory.create_building("CastleUpgradeStation", upgrade_station_pos))
        
        # Initialize animation system
        self.animation_manager = AnimationManager()
        
        # Initialize UI with play/pause button and game speed slider
        self.game_ui = GameUI(screen)
        self.building_menu = BuildingMenu(screen)
        self.tower_menu = TowerMenu(screen)
        self.tower_placement_ui = TowerPlacementUI(screen, self)
        
        # Add castle menu
        self.castle_menu = CastleMenu(screen)
        
        # Add developer menu
        self.dev_menu = DeveloperMenu(screen, self)
        
        # Initialize save manager
        self.save_manager = SaveManager(self)
        
        # Game state variables
        self.selected_entity = None
        
        # Initialize state manager
        self.state_manager = GameStateManager(self)
        # Create states dictionary for access by state objects
        self.states = {}
        
        # Add states to manager
        self.state_manager.add_state("main_menu", MainMenuState)
        self.states["main_menu"] = self.state_manager.states["main_menu"]
        
        self.state_manager.add_state("playing", PlayingState)
        self.states["playing"] = self.state_manager.states["playing"]
        
        self.state_manager.add_state("paused", PausedState)
        self.states["paused"] = self.state_manager.states["paused"]
        
        self.state_manager.add_state("tower_placement", TowerPlacementState)
        self.states["tower_placement"] = self.state_manager.states["tower_placement"]
        
        self.state_manager.add_state("game_over", GameOverState)
        self.states["game_over"] = self.state_manager.states["game_over"]
        
        # Start with main menu state
        self.state_manager.change_state("main_menu")
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Apply time scaling to dt
            raw_dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            dt = raw_dt * self.time_scale  # Apply time scale for speed control
            
            # Collect all events once
            events = pygame.event.get()
            self.handle_events(events)
            
            # If game is running, update state
            if self.running:
                self.update(dt, raw_dt)
                self.draw()
                pygame.display.flip()
    
    def handle_events(self, events):
        """
        Process pygame events
        
        Args:
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Check for developer menu toggle (Ctrl+D)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.dev_menu.toggle()
                return
            
            # Handle developer menu events first if it's visible
            if self.dev_menu.visible:
                self.dev_menu.handle_event(event)  # Pass a single event, not the list
                continue
        
        # Let the current state handle events if dev menu didn't handle them
        if self.dev_menu.visible:
            return
            
        self.state_manager.handle_events(events)
    
    def update(self, dt, raw_dt=None):
        """
        Update game state
        
        Args:
            dt: Time delta in seconds (with time scaling)
            raw_dt: Raw time delta without scaling, for dev menu
        """
        # Developer menu always updates with raw dt (not affected by time scale)
        if raw_dt:
            self.dev_menu.update(raw_dt)
        
        # Set pause state for buildings
        if self.state_manager.current_state is self.states["paused"]:
            for building in self.buildings:
                if hasattr(building, 'update'):
                    # Update buildings with game_paused=True
                    building.update(0, self.resource_manager, raw_dt, True)
        
        # Update current state
        self.state_manager.update(dt)
    
    def draw(self):
        """Draw current game state to screen"""
        # Let the current state draw
        self.state_manager.draw(self.screen)
        
        # Developer menu draws on top of everything if visible
        if self.dev_menu.visible:
            self.dev_menu.draw()
    
    def enter_tower_placement_mode(self, tower_type):
        """
        Enter tower placement mode for specified tower type
        
        Args:
            tower_type: Type of tower to place
        """
        self.state_manager.change_state("tower_placement")
        tower_placement_state = self.state_manager.states["tower_placement"]
        tower_placement_state.set_tower_type(tower_type)
    
    def is_valid_tower_position(self, position):
        """
        Check if position is valid for tower placement
        
        Args:
            position: Tuple of (x, y) coordinates
            
        Returns:
            True if position is valid, False otherwise
        """
        # Create a rect for the tower at this position
        tower_ref_size = (40, 40)  # Defined in reference dimensions
        tower_size = scale_size(tower_ref_size)
        tower_rect = pygame.Rect(
            position[0] - tower_size[0] // 2,
            position[1] - tower_size[1] // 2,
            tower_size[0],
            tower_size[1]
        )
        
        # Check if tower is within castle boundaries
        if not self.castle.is_position_within_castle(position):
            return False
        
        # Check collision with buildings
        for building in self.buildings:
            if tower_rect.colliderect(building.rect):
                return False
        
        # Check collision with other towers
        for tower in self.towers:
            if tower_rect.colliderect(tower.rect):
                return False
        
        return True
    
    def reset_castle(self):
        """
        Restore castle health after game over
        """
        self.castle.health = self.castle.max_health
    
    def set_wave(self, wave_number):
        """
        Set the current wave number
        
        Args:
            wave_number: New wave number
        """
        # Set wave manager's wave number
        self.wave_manager.current_wave = wave_number
        
        # Reset wave state
        self.wave_manager.active_monsters = []
        self.wave_manager.wave_active = False
        self.wave_manager.wave_completed = True
        self.wave_manager.monsters_to_spawn = 0
    
    # Helper function to get the game instance
    @staticmethod
    def get_instance():
        """
        Get the current game instance (for use in other modules)
        
        Returns:
            Current Game instance or None
        """
        return game_instance
