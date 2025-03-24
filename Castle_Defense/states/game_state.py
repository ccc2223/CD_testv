# states/game_state.py
"""
Base game state class and state manager for Castle Defense
"""
from abc import ABC, abstractmethod

class GameState(ABC):
    """
    Abstract base class for all game states
    """
    def __init__(self, game):
        """
        Initialize with reference to the game instance
        
        Args:
            game: Game instance
        """
        self.game = game
    
    @abstractmethod
    def handle_events(self, events):
        """
        Handle all pygame events
        
        Args:
            events: List of pygame events
            
        Returns:
            Boolean indicating if events were handled
        """
        pass
    
    @abstractmethod
    def update(self, dt):
        """
        Update state logic
        
        Args:
            dt: Time delta in seconds
        """
        pass
    
    @abstractmethod
    def draw(self, screen):
        """
        Draw state to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        pass
    
    def enter(self):
        """
        Called when entering this state
        """
        pass
    
    def exit(self):
        """
        Called when exiting this state
        """
        pass


class GameStateManager:
    """
    Manages game states and transitions between them
    """
    def __init__(self, game):
        """
        Initialize the state manager
        
        Args:
            game: Game instance
        """
        self.game = game
        self.states = {}
        self.current_state = None
    
    def add_state(self, state_id, state_class, *args, **kwargs):
        """
        Add a state to the manager
        
        Args:
            state_id: String identifier for the state
            state_class: GameState class
            *args, **kwargs: Arguments to pass to state constructor
        """
        self.states[state_id] = state_class(self.game, *args, **kwargs)
    
    def change_state(self, state_id):
        """
        Change to a different state
        
        Args:
            state_id: String identifier for the new state
            
        Returns:
            Boolean indicating if state change was successful
        """
        if state_id not in self.states:
            return False
        
        if self.current_state:
            self.current_state.exit()
        
        self.current_state = self.states[state_id]
        self.current_state.enter()
        return True
    
    def handle_events(self, events):
        """
        Delegate event handling to current state
        
        Args:
            events: List of pygame events
        """
        if self.current_state:
            return self.current_state.handle_events(events)
        return False
    
    def update(self, dt):
        """
        Update current state
        
        Args:
            dt: Time delta in seconds
        """
        if self.current_state:
            self.current_state.update(dt)
    
    def draw(self, screen):
        """
        Draw current state
        
        Args:
            screen: Pygame surface to draw on
        """
        if self.current_state:
            self.current_state.draw(screen)
