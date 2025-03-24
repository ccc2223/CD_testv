# states/playing_state.py
"""
Playing state for Castle Defense - handles main gameplay
"""
import pygame
from .game_state import GameState
# Import the building classes directly
from features.buildings import Mine, Coresmith, CastleUpgradeStation

class PlayingState(GameState):
    """
    Main gameplay state where the player defends the castle
    """
    def __init__(self, game):
        """
        Initialize playing state
        
        Args:
            game: Game instance
        """
        super().__init__(game)
        # Store references to commonly used components for cleaner code
        self.castle = self.game.castle
        self.wave_manager = self.game.wave_manager
        self.resource_manager = self.game.resource_manager
        self.animation_manager = self.game.animation_manager
        self.buildings = self.game.buildings
        self.towers = self.game.towers
        
        # Track if game is paused
        self.paused = False
    
    def handle_events(self, events):
        """
        Handle gameplay events
        
        Args:
            events: List of pygame events
            
        Returns:
            Boolean indicating if events were handled
        """
        # First let the game UI handle events
        for event in events:
            if self.game.game_ui.handle_event(event):
                return True
        
        for event in events:
            # Space to start next wave
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.wave_manager.start_next_wave()
                # Escape to pause
                elif event.key == pygame.K_ESCAPE:
                    self.game.state_manager.change_state("paused")
                    # Update the UI play/pause button state
                    self.game.game_ui.is_paused = True
                    self.game.game_ui.play_pause_button.text = "▶"  # Play icon
                    return True
            
            # Check for building and tower clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if tower placement UI is clicked
                if self.game.tower_placement_ui.handle_event(event):
                    # Tower placement UI handled the event
                    continue
                
                # Check if clicking on a building
                building_clicked = False
                for building in self.buildings:
                    if building.rect.collidepoint(mouse_pos):
                        # Deselect previous entity
                        if self.game.selected_entity and hasattr(self.game.selected_entity, 'selected'):
                            self.game.selected_entity.selected = False
                            
                        self.game.selected_entity = building
                        # Use the imported class types directly for instanceof checks
                        if isinstance(building, Mine):
                            self.game.building_menu.set_building(building, "mine", self.resource_manager)
                            self.game.building_menu.toggle()
                        elif isinstance(building, Coresmith):
                            self.game.building_menu.set_building(building, "coresmith", self.resource_manager)
                            self.game.building_menu.toggle()
                        elif isinstance(building, CastleUpgradeStation):
                            # Open the castle menu for the upgrade station
                            self.game.castle_menu.set_castle(self.castle, self.resource_manager)
                            self.game.castle_menu.toggle()
                        building_clicked = True
                        break
                
                if not building_clicked:
                    # Check if clicking on a tower
                    tower_clicked = False
                    for tower in self.towers:
                        if tower.rect.collidepoint(mouse_pos):
                            # Deselect previous entity
                            if self.game.selected_entity and hasattr(self.game.selected_entity, 'selected'):
                                self.game.selected_entity.selected = False
                            
                            self.game.selected_entity = tower
                            tower.selected = True  # Set selected flag for range display
                            self.game.tower_menu.set_tower(tower, self.resource_manager)
                            self.game.tower_menu.toggle()
                            tower_clicked = True
                            break
                    
                    if not tower_clicked:
                        # Check for deselection
                        if self.game.selected_entity and hasattr(self.game.selected_entity, 'selected'):
                            self.game.selected_entity.selected = False
                            self.game.selected_entity = None
                            
                        # Handle menu clicks
                        self.game.building_menu.handle_event(event)
                        self.game.tower_menu.handle_event(event)
                        self.game.castle_menu.handle_event(event)
        
        return False
    
    def update(self, dt):
        """
        Update gameplay logic
        
        Args:
            dt: Time delta in seconds
        """
        # Update game UI
        self.game.game_ui.update(dt)
        
        # Update animation manager
        self.animation_manager.update(dt)
        
        # Update castle
        self.castle.update(dt)
        
        # Get the raw (unscaled) dt for buildings to maintain consistent production
        raw_dt = dt / self.game.time_scale if self.game.time_scale > 0 else dt
        
        # Update buildings - use raw_dt for consistent production regardless of game speed
        # Also pass the pause state
        for building in self.buildings:
            building.update(dt, self.resource_manager, raw_dt, self.paused)
        
        # Update wave manager and monsters
        self.wave_manager.update(dt, self.castle, self.animation_manager)
        
        # Update towers
        for tower in self.towers:
            tower.update(dt, self.wave_manager.active_monsters, self.animation_manager)
        
        # Check for auto-save
        self.game.save_manager.check_autosave()
        
        # Check for game over
        if self.castle.health <= 0:
            self.game.state_manager.change_state("game_over")
        
        # Continuous wave mode (from developer menu)
        if hasattr(self.wave_manager, 'continuous_wave') and self.wave_manager.continuous_wave:
            if self.wave_manager.wave_completed and not self.wave_manager.wave_active:
                self.wave_manager.start_next_wave()
    
    def draw(self, screen):
        """
        Draw gameplay elements to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Clear screen with background color
        screen.fill(self.game.BACKGROUND_COLOR)
        
        # Draw castle first (as the base area)
        self.castle.draw(screen)
        
        # Draw buildings
        for building in self.buildings:
            building.draw(screen)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(screen)
        
        # Draw monsters
        self.wave_manager.draw(screen)
        
        # Draw animations (particles, effects)
        self.animation_manager.draw(screen)
        
        # Draw UI
        self.game.game_ui.draw(self.resource_manager, self.castle, self.wave_manager)
        
        # Draw tower placement UI
        self.game.tower_placement_ui.draw(self.resource_manager)
        
        # Draw menus
        self.game.building_menu.draw()
        self.game.tower_menu.draw()
        self.game.castle_menu.draw()
        
        # Draw game speed indicator if not at normal speed
        if self.game.time_scale != 1.0:
            font = pygame.font.Font(None, self.game.scale_value(24))
            speed_text = f"Game Speed: {self.game.time_scale:.1f}x"
            speed_color = (255, 200, 100) if self.game.time_scale > 1.0 else (100, 200, 255)
            speed_surface = font.render(speed_text, True, speed_color)
            speed_rect = speed_surface.get_rect(topright=(self.game.WINDOW_WIDTH - 20, 20))
            screen.blit(speed_surface, speed_rect)
