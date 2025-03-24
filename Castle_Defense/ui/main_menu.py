# ui/main_menu.py
"""
Main menu UI for Castle Defense game.
"""
import pygame
import os
import math
import random
from effects.particles import ParticleSystem, Particle
from utils import scale_position, scale_size, scale_value
from ui.menus import Button

class MainMenu:
    """Main menu for Castle Defense game"""
    def __init__(self, screen, game_instance):
        """
        Initialize main menu
        
        Args:
            screen: Pygame surface to draw on
            game_instance: Game instance for callbacks
        """
        self.screen = screen
        self.game = game_instance
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, scale_value(80))
        self.button_font = pygame.font.Font(None, scale_value(36))
        self.info_font = pygame.font.Font(None, scale_value(24))
        
        # Setup dimensions
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Calculate positions for title and buttons
        self.title_pos = (self.width // 2, self.height // 4)
        button_center_y = self.height // 2 + scale_value(50)
        button_spacing = scale_value(80)
        
        # Create buttons
        button_width = scale_value(250)
        button_height = scale_value(60)
        
        # Create buttons with medieval style
        self.new_game_button = StoneButton(
            (self.width // 2 - button_width // 2, button_center_y - button_spacing),
            (button_width, button_height),
            "New Game",
            self.start_new_game
        )
        
        self.load_game_button = StoneButton(
            (self.width // 2 - button_width // 2, button_center_y + button_spacing),
            (button_width, button_height),
            "Load Game",
            self.show_load_game
        )
        
        # Initialize title animation
        self.title_blocks = []
        self.create_title_animation()
        
        # Initialize load game panel
        self.load_panel = LoadGamePanel(screen, game_instance)
        self.show_load_panel = False
        
        # Initialize particle system for visual effects
        self.particle_system = ParticleSystem()
        
        # Initialize background elements
        self.castle_parts = []
        self.clouds = []
        self.flags = []
        self.mountain_points = []
        
        # Generate mountain silhouette once
        self.generate_mountains()
        
        # Create castle elements
        self.create_background_elements()
        
        # Animation timers
        self.time = 0
        self.title_animation_complete = False
        self.title_glow_intensity = 0
        
        # Tower firing animation
        self.tower_fire_timer = random.uniform(3, 5)
    
    def create_title_animation(self):
        """Create animated title blocks"""
        title_text = "Castle Defense"
        text_surface = self.title_font.render(title_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.title_pos)
        
        # Create blocks for each letter
        block_width = scale_value(25)
        block_height = scale_value(30)
        
        for i, char in enumerate(title_text):
            if char == ' ':
                continue
                
            # Calculate position for this character
            char_surface = self.title_font.render(char, True, (255, 240, 200))
            char_width = char_surface.get_width()
            
            # Calculate starting position (off-screen, above final position)
            final_x = text_rect.left + text_surface.get_width() * (i / len(title_text))
            final_y = self.title_pos[1]
            
            # Random starting position above the screen
            start_y = -random.randint(100, 500)
            
            self.title_blocks.append({
                'char': char,
                'surface': char_surface,
                'start_pos': (final_x, start_y),
                'final_pos': (final_x, final_y),
                'current_pos': (final_x, start_y),
                'start_delay': i * 0.1,  # Stagger the start time
                'speed': random.uniform(2.0, 3.0),
                'landed': False
            })
    
    def generate_mountains(self):
        """Generate static mountain points"""
        # Base mountain height
        mountain_y = self.height * 0.7
        
        # Start with leftmost point
        self.mountain_points = [(0, mountain_y)]
        
        # Generate mountain peaks
        x = 0
        while x < self.width:
            # Mountain peak
            peak_height = random.randint(50, 150)
            peak_width = random.randint(100, 300)
            
            self.mountain_points.append((x + peak_width // 2, mountain_y - peak_height))
            x += peak_width
        
        # Close the polygon
        self.mountain_points.append((self.width, mountain_y))
        self.mountain_points.append((self.width, self.height))
        self.mountain_points.append((0, self.height))
    
    def create_background_elements(self):
        """Create castle and background decorative elements"""
        # Create clouds
        for _ in range(5):
            self.clouds.append({
                'x': random.randint(0, self.width),
                'y': random.randint(50, self.height // 3),
                'width': random.randint(100, 200),
                'speed': random.uniform(2, 10),
                'alpha': random.randint(100, 180)
            })
        
        # Create castle walls and towers
        castle_base_y = self.height * 0.75
        wall_width = self.width * 0.8
        wall_left = (self.width - wall_width) // 2
        
        # Main castle wall
        self.castle_parts.append({
            'type': 'wall',
            'rect': pygame.Rect(wall_left, castle_base_y, wall_width, self.height * 0.15),
            'color': (100, 90, 80)
        })
        
        # Castle towers
        tower_width = scale_value(80)
        tower_height = scale_value(150)
        
        # Left tower
        left_tower_x = wall_left - tower_width // 2
        self.castle_parts.append({
            'type': 'tower',
            'rect': pygame.Rect(left_tower_x, castle_base_y - tower_height + scale_value(40), 
                              tower_width, tower_height),
            'color': (80, 70, 60),
            'fire_position': (left_tower_x + tower_width // 2, castle_base_y - tower_height + scale_value(50)),
            'can_fire': True
        })
        
        # Right tower
        right_tower_x = wall_left + wall_width - tower_width // 2
        self.castle_parts.append({
            'type': 'tower',
            'rect': pygame.Rect(right_tower_x, castle_base_y - tower_height + scale_value(40), 
                              tower_width, tower_height),
            'color': (80, 70, 60),
            'fire_position': (right_tower_x + tower_width // 2, castle_base_y - tower_height + scale_value(50)),
            'can_fire': True
        })
        
        # Center tower (main keep)
        center_tower_width = scale_value(120)
        center_tower_height = scale_value(200)
        center_tower_x = self.width // 2 - center_tower_width // 2
        
        self.castle_parts.append({
            'type': 'tower',
            'rect': pygame.Rect(center_tower_x, castle_base_y - center_tower_height + scale_value(40), 
                              center_tower_width, center_tower_height),
            'color': (90, 80, 70),
            'fire_position': (center_tower_x + center_tower_width // 2, castle_base_y - center_tower_height + scale_value(60)),
            'can_fire': True
        })
        
        # Add flags
        self.flags.append({
            'x': center_tower_x + center_tower_width // 2,
            'y': castle_base_y - center_tower_height + scale_value(30),
            'width': scale_value(30),
            'height': scale_value(40),
            'color': (200, 50, 50),
            'wave_time': 0
        })
        
        self.flags.append({
            'x': left_tower_x + tower_width // 2,
            'y': castle_base_y - tower_height + scale_value(30),
            'width': scale_value(25),
            'height': scale_value(30),
            'color': (50, 50, 200),
            'wave_time': 0.5  # Offset wave animation
        })
        
        self.flags.append({
            'x': right_tower_x + tower_width // 2,
            'y': castle_base_y - tower_height + scale_value(30),
            'width': scale_value(25),
            'height': scale_value(30),
            'color': (50, 50, 200),
            'wave_time': 1.0  # Offset wave animation
        })
    
    def update(self, dt):
        """
        Update menu state
        
        Args:
            dt: Time delta in seconds
        """
        self.time += dt
        
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        self.new_game_button.update(mouse_pos)
        self.load_game_button.update(mouse_pos)
        
        # Update title animation
        if not self.title_animation_complete:
            all_landed = True
            for block in self.title_blocks:
                if not block['landed']:
                    # Check if it's time to start this block's animation
                    if self.time > block['start_delay']:
                        # Move block down
                        distance_y = block['final_pos'][1] - block['current_pos'][1]
                        move_y = min(distance_y, block['speed'] * scale_value(100) * dt)
                        
                        block['current_pos'] = (
                            block['current_pos'][0],
                            block['current_pos'][1] + move_y
                        )
                        
                        # Check if block has reached its final position
                        if abs(block['current_pos'][1] - block['final_pos'][1]) < 2:
                            block['landed'] = True
                            block['current_pos'] = block['final_pos']
                            
                            # Create impact particles
                            self.create_impact_particles(block['final_pos'])
                    
                    all_landed = False
            
            if all_landed:
                self.title_animation_complete = True
        
        # Update title glow
        if self.title_animation_complete:
            self.title_glow_intensity = 0.4 + 0.2 * math.sin(self.time * 2)
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Occasionally fire from towers
        self.tower_fire_timer -= dt
        if self.tower_fire_timer <= 0:
            # Reset timer
            self.tower_fire_timer = random.uniform(2, 5)
            
            # Find a tower that can fire
            can_fire_towers = [tower for tower in self.castle_parts if tower['type'] == 'tower' and tower.get('can_fire', False)]
            if can_fire_towers:
                tower = random.choice(can_fire_towers)
                self.fire_from_tower(tower['fire_position'])
        
        # Update clouds
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed'] * dt
            if cloud['x'] + cloud['width'] < 0:
                cloud['x'] = self.width + random.randint(50, 200)
                cloud['y'] = random.randint(50, self.height // 3)
        
        # Update flags
        for flag in self.flags:
            flag['wave_time'] += dt
            
        # If load panel is shown, update it
        if self.show_load_panel:
            self.load_panel.update(dt)
    
    def create_impact_particles(self, position):
        """
        Create particles for block impact
        
        Args:
            position: Position for particles
        """
        num_particles = random.randint(5, 10)
        for _ in range(num_particles):
            # Random velocity
            angle = random.uniform(0, math.pi * 2)
            speed = scale_value(random.uniform(50, 150))
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            # Stone-like colors
            color = (
                random.randint(180, 220),
                random.randint(170, 210),
                random.randint(150, 190)
            )
            
            # Create particle
            particle = Particle(
                position,
                color,
                random.uniform(2, 4),
                random.uniform(0.3, 0.6),
                velocity=(vel_x, vel_y),
                gravity=scale_value(300)
            )
            self.particle_system.add_particle(particle)
    
    def fire_from_tower(self, position):
        """
        Create projectile firing from tower
        
        Args:
            position: Tower position to fire from
        """
        # Random target position (above horizon)
        target_x = random.randint(0, self.width)
        target_y = random.randint(50, self.height // 3)
        
        # Create arrow effect
        self.create_tower_arrow(position, (target_x, target_y))
    
    def create_tower_arrow(self, start_pos, target_pos):
        """
        Create arrow projectile from tower
        
        Args:
            start_pos: Starting position
            target_pos: Target position
        """
        # Calculate direction and distance
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            return
        
        # Normalize direction
        dx /= distance
        dy /= distance
        
        # Calculate velocity
        speed = scale_value(300)
        vel_x = dx * speed
        vel_y = dy * speed
        
        # Create projectile particle
        arrow = Particle(
            start_pos,
            (200, 200, 200),
            3,
            1.0,
            velocity=(vel_x, vel_y)
        )
        self.particle_system.add_particle(arrow)
        
        # Create a few trail particles
        for _ in range(3):
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)
            
            trail = Particle(
                (start_pos[0] + offset_x, start_pos[1] + offset_y),
                (150, 150, 150),
                2,
                0.5,
                velocity=(vel_x * 0.8, vel_y * 0.8)
            )
            self.particle_system.add_particle(trail)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        # If load panel is shown, let it handle events first
        if self.show_load_panel:
            if self.load_panel.handle_event(event):
                return True
            
            # Check for clicking outside panel to close it
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.load_panel.panel_rect.collidepoint(event.pos):
                    self.show_load_panel = False
                    return True
            
            # Check for Escape key to close panel
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_load_panel = False
                return True
                
            return False
        
        # Regular button handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.new_game_button.rect.collidepoint(event.pos):
                self.new_game_button.click()
                return True
            
            elif self.load_game_button.rect.collidepoint(event.pos):
                self.load_game_button.click()
                return True
        
        return False
    
    def draw(self):
        """Draw menu to screen"""
        # Draw sky gradient background
        self.draw_sky_background()
        
        # Draw distant mountains
        self.draw_mountains()
        
        # Draw clouds
        self.draw_clouds()
        
        # Draw castle and decorations
        self.draw_castle()
        
        # Draw flags
        self.draw_flags()
        
        # Draw title
        self.draw_title()
        
        # Draw buttons
        self.new_game_button.draw(self.screen)
        self.load_game_button.draw(self.screen)
        
        # Draw particle effects
        self.particle_system.draw(self.screen)
        
        # Draw info text
        info_text = "Press ESC to exit"
        info_surface = self.info_font.render(info_text, True, (200, 200, 200))
        info_rect = info_surface.get_rect(bottomright=(self.width - 20, self.height - 20))
        self.screen.blit(info_surface, info_rect)
        
        # Draw load game panel if visible
        if self.show_load_panel:
            self.load_panel.draw()
    
    def draw_sky_background(self):
        """Draw gradient sky background"""
        # Create gradient from dark blue to light blue
        for y in range(0, self.height, 2):  # Draw every other line for performance
            # Calculate color based on height
            ratio = y / self.height
            r = int(20 + 80 * ratio)
            g = int(30 + 120 * ratio)
            b = int(80 + 120 * ratio)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y), 2)
    
    def draw_mountains(self):
        """Draw static mountains"""
        # Draw the pre-generated mountain silhouette
        mountain_color = (60, 70, 80)
        pygame.draw.polygon(self.screen, mountain_color, self.mountain_points)
    
    def draw_clouds(self):
        """Draw clouds in the sky"""
        for cloud in self.clouds:
            # Create a semi-transparent surface for the cloud
            cloud_width = scale_value(cloud['width'])
            cloud_height = scale_value(cloud['width'] // 2)
            cloud_surface = pygame.Surface((cloud_width, cloud_height), pygame.SRCALPHA)
            
            # Draw cloud as a series of overlapping circles
            num_circles = int(cloud_width / 20)
            for i in range(num_circles):
                radius = cloud_height * 0.6
                x = (i * cloud_width // num_circles) + random.randint(-5, 5)
                y = cloud_height // 2 + random.randint(-5, 5)
                
                pygame.draw.circle(
                    cloud_surface, 
                    (255, 255, 255, cloud['alpha']), 
                    (x, y), 
                    radius
                )
            
            # Draw cloud
            self.screen.blit(cloud_surface, (cloud['x'], cloud['y']))
    
    def draw_castle(self):
        """Draw castle walls and towers"""
        # Draw all castle parts
        for part in self.castle_parts:
            pygame.draw.rect(self.screen, part['color'], part['rect'])
            
            # Add details based on part type
            if part['type'] == 'wall':
                # Draw crenellations
                wall_top = part['rect'].top
                wall_left = part['rect'].left
                wall_width = part['rect'].width
                
                crenel_width = scale_value(20)
                crenel_height = scale_value(15)
                crenel_spacing = scale_value(30)
                
                x = wall_left
                while x < wall_left + wall_width:
                    pygame.draw.rect(
                        self.screen,
                        part['color'],
                        (x, wall_top - crenel_height, crenel_width, crenel_height)
                    )
                    x += crenel_width + crenel_spacing
            
            elif part['type'] == 'tower':
                # Draw tower top (crenellations)
                tower_top = part['rect'].top
                tower_left = part['rect'].left
                tower_width = part['rect'].width
                
                crenel_width = scale_value(10)
                crenel_height = scale_value(10)
                crenel_spacing = scale_value(15)
                
                x = tower_left
                while x < tower_left + tower_width:
                    pygame.draw.rect(
                        self.screen,
                        part['color'],
                        (x, tower_top - crenel_height, crenel_width, crenel_height)
                    )
                    x += crenel_width + crenel_spacing
                
                # Draw tower window
                window_width = tower_width // 3
                window_height = tower_width // 3
                window_x = tower_left + (tower_width - window_width) // 2
                window_y = tower_top + tower_width // 2
                
                pygame.draw.rect(
                    self.screen,
                    (40, 40, 40),
                    (window_x, window_y, window_width, window_height)
                )
    
    def draw_flags(self):
        """Draw animated flags on castle towers"""
        for flag in self.flags:
            # Calculate flag wave
            wave_factor = math.sin(flag['wave_time'] * 5) * 0.2
            
            # Create flag points
            points = [
                (flag['x'], flag['y']),  # Pole attachment point
                (flag['x'] + flag['width'], flag['y'] + flag['height'] * wave_factor),  # Top corner
                (flag['x'] + flag['width'], flag['y'] + flag['height'] * (1 + wave_factor * 0.5)),  # Bottom corner
                (flag['x'], flag['y'] + flag['height'])  # Bottom attachment point
            ]
            
            # Draw flag
            pygame.draw.polygon(self.screen, flag['color'], points)
            
            # Draw flag pole
            pygame.draw.line(
                self.screen,
                (100, 100, 100),
                (flag['x'], flag['y'] - scale_value(20)),
                (flag['x'], flag['y'] + flag['height']),
                scale_value(3)
            )
    
    def draw_title(self):
        """Draw animated title"""
        if self.title_animation_complete:
            # Draw complete title with glow effect
            # Create a larger surface for the glow
            glow_size = scale_value(4)  # Glow size in pixels
            glow_alpha = int(100 * self.title_glow_intensity)
            
            for block in self.title_blocks:
                char_pos = block['current_pos']
                char_surface = block['surface']
                
                # Draw glow around the character
                glow_surface = pygame.Surface(
                    (char_surface.get_width() + glow_size*2, 
                     char_surface.get_height() + glow_size*2),
                    pygame.SRCALPHA
                )
                
                # Draw glowing version of the character
                glow_color = (255, 200, 100, glow_alpha)  # Soft orange glow
                
                # Draw the glow character
                glow_char = self.title_font.render(block['char'], True, glow_color)
                
                # Draw the glow character multiple times with offset for blur effect
                for offset_x in range(-glow_size, glow_size+1, 2):
                    for offset_y in range(-glow_size, glow_size+1, 2):
                        glow_surface.blit(glow_char, (offset_x + glow_size, offset_y + glow_size))
                
                # Blit the glow surface first
                glow_rect = glow_surface.get_rect(center=(char_pos[0], char_pos[1]))
                self.screen.blit(glow_surface, glow_rect)
                
                # Then blit the actual character on top
                char_rect = char_surface.get_rect(center=(char_pos[0], char_pos[1]))
                self.screen.blit(char_surface, char_rect)
                
                # Randomly create an ambient particle near the title
                if random.random() < 0.02:
                    self.create_ambient_title_particle(char_pos)
        else:
            # Draw falling blocks
            for block in self.title_blocks:
                if self.time > block['start_delay']:
                    char_pos = block['current_pos']
                    char_surface = block['surface']
                    
                    char_rect = char_surface.get_rect(center=(char_pos[0], char_pos[1]))
                    self.screen.blit(char_surface, char_rect)
    
    def create_ambient_title_particle(self, position):
        """
        Create ambient particle near title
        
        Args:
            position: Position to create particle
        """
        # Random position near the character
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-10, 10)
        pos = (position[0] + offset_x, position[1] + offset_y)
        
        # Upward drift
        vel_y = scale_value(random.uniform(-20, -10))
        vel_x = scale_value(random.uniform(-5, 5))
        
        # Golden sparkle
        color = (
            random.randint(200, 255),
            random.randint(150, 200),
            random.randint(50, 100)
        )
        
        # Create particle
        particle = Particle(
            pos,
            color,
            random.uniform(1, 2),
            random.uniform(0.5, 1.5),
            velocity=(vel_x, vel_y)
        )
        self.particle_system.add_particle(particle)
    
    def start_new_game(self):
        """Start a new game"""
        # Change to playing state to start new game
        self.game.state_manager.change_state("playing")
    
    def show_load_game(self):
        """Show load game panel"""
        self.show_load_panel = True
        self.load_panel.refresh_save_list()


class StoneButton(Button):
    """Medieval-style stone button for main menu"""
    def __init__(self, position, size, text, callback):
        """
        Initialize stone button
        
        Args:
            position: Tuple of (x, y) position for top-left corner
            size: Tuple of (width, height)
            text: Button text
            callback: Function to call when clicked
        """
        super().__init__(position, size, text, callback)
        
        # Override default colors for stone appearance
        self.color = (90, 90, 90)
        self.hover_color = (110, 110, 110)
        self.text_color = (220, 220, 200)
        
        # Add stone texture effect
        self.texture_dots = []
        
        # Generate random dots for stone texture
        num_dots = int(size[0] * size[1] / 100)
        for _ in range(num_dots):
            self.texture_dots.append((
                random.randint(0, size[0]),
                random.randint(0, size[1]),
                random.randint(0, 20)  # Darkness value
            ))
        
        # Animation properties
        self.press_offset = 0
        self.press_animation = 0
        
        # Use a larger font
        self.font = pygame.font.Font(None, scale_value(28))
    
    def click(self):
        """Handle button click with animation"""
        # Start press animation
        self.press_animation = 0.2  # Animation duration in seconds
        
        # Call the callback
        super().click()
    
    def update(self, mouse_pos):
        """
        Update button state
        
        Args:
            mouse_pos: Current mouse position
        """
        super().update(mouse_pos)
        
        # Update press animation
        if self.press_animation > 0:
            self.press_animation -= 0.02
            self.press_offset = 4 * self.press_animation
        else:
            self.press_animation = 0
            self.press_offset = 0
    
    def draw(self, screen):
        """
        Draw the stone button
        
        Args:
            screen: Surface to draw on
        """
        # Determine current color based on state
        if self.disabled:
            color = self.disabled_color
        else:
            color = self.hover_color if self.hovered else self.color
        
        # Apply pressed offset to position
        draw_rect = pygame.Rect(
            self.rect.left,
            self.rect.top + self.press_offset,
            self.rect.width,
            self.rect.height - self.press_offset
        )
        
        # Draw button with slight 3D effect
        pygame.draw.rect(screen, (50, 50, 50), 
                        (self.rect.left - 2, self.rect.top - 2, 
                         self.rect.width + 4, self.rect.height + 4))
        
        pygame.draw.rect(screen, color, draw_rect)
        
        # Draw stone texture
        for dot in self.texture_dots:
            x, y, darkness = dot
            x += self.rect.left
            y += self.rect.top + self.press_offset
            
            # Only draw if within button bounds
            if draw_rect.collidepoint(x, y):
                dot_color = (max(0, color[0] - darkness), 
                             max(0, color[1] - darkness), 
                             max(0, color[2] - darkness))
                
                screen.set_at((int(x), int(y)), dot_color)
        
        # Draw button text with slight shadow
        text_color = (150, 150, 150) if self.disabled else self.text_color
        
        # Draw text shadow
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(draw_rect.centerx + 2, draw_rect.centery + 2))
        screen.blit(text_surface, text_rect)
        
        # Draw text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=draw_rect.center)
        screen.blit(text_surface, text_rect)
        
        # Draw outline
        pygame.draw.rect(screen, (50, 50, 50), draw_rect, 1)
        
        # Draw a subtle glow effect if hovered
        if self.hovered and not self.disabled:
            glow_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 255, 200, 50), 
                            (0, 0, draw_rect.width, draw_rect.height), 2)
            screen.blit(glow_surf, draw_rect)


class LoadGamePanel:
    """Panel for loading saved games"""
    def __init__(self, screen, game_instance):
        """
        Initialize load game panel
        
        Args:
            screen: Pygame surface to draw on
            game_instance: Game instance for callbacks
        """
        self.screen = screen
        self.game = game_instance
        
        # Panel dimensions
        panel_width = int(screen.get_width() * 0.6)
        panel_height = int(screen.get_height() * 0.7)
        
        self.panel_rect = pygame.Rect(
            (screen.get_width() - panel_width) // 2,
            (screen.get_height() - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, scale_value(36))
        self.item_font = pygame.font.Font(None, scale_value(24))
        
        # Save items and buttons
        self.save_items = []
        self.load_buttons = []
        self.delete_buttons = []
        
        # Selected save
        self.selected_save = None
        
        # Animation properties
        self.animation_progress = 0  # 0 to 1 for opening animation
        
        # Initialize save list
        self.refresh_save_list()
    
    def refresh_save_list(self):
        """Refresh the list of available save files"""
        # Clear existing items
        self.save_items = []
        self.load_buttons = []
        self.delete_buttons = []
        
        # Get save files
        save_dir = self.game.save_manager.save_directory
        try:
            save_files = [f for f in os.listdir(save_dir) if f.endswith('.save')]
            save_files.sort(reverse=True)  # Most recent first
        except (FileNotFoundError, PermissionError):
            save_files = []
        
        # Create items for each save file
        item_height = scale_value(50)
        spacing = scale_value(10)
        
        y = self.panel_rect.top + scale_value(60)
        for i, save_file in enumerate(save_files):
            # Parse save filename for display
            # Format: Date-Time-WaveXXX.save
            try:
                date_time, wave = save_file.rsplit('-', 1)
                wave = wave.replace('Wave', '').replace('.save', '')
                display_text = f"{date_time} - Wave {wave}"
            except ValueError:
                display_text = save_file
            
            # Create save item
            item_rect = pygame.Rect(
                self.panel_rect.left + spacing,
                y,
                self.panel_rect.width - spacing * 2,
                item_height
            )
            
            self.save_items.append({
                'filename': save_file,
                'display': display_text,
                'rect': item_rect,
                'selected': False
            })
            
            # Create load button
            load_button = Button(
                (self.panel_rect.right - spacing - scale_value(100) - scale_value(100) - spacing, y + scale_value(10)),
                (scale_value(100), scale_value(30)),
                "Load",
                lambda f=save_file: self.load_game(f)
            )
            self.load_buttons.append(load_button)
            
            # Create delete button
            delete_button = Button(
                (self.panel_rect.right - spacing - scale_value(100), y + scale_value(10)),
                (scale_value(100), scale_value(30)),
                "Delete",
                lambda f=save_file: self.delete_save(f)
            )
            self.delete_buttons.append(delete_button)
            
            y += item_height + spacing
    
    def update(self, dt):
        """
        Update panel state
        
        Args:
            dt: Time delta in seconds
        """
        # Update opening animation
        if self.animation_progress < 1:
            self.animation_progress = min(1, self.animation_progress + dt * 3)
        
        # Update buttons
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.load_buttons:
            button.update(mouse_pos)
        
        for button in self.delete_buttons:
            button.update(mouse_pos)
        
        # Check for save selection
        for item in self.save_items:
            item['selected'] = item['rect'].collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.load_buttons):
                if button.rect.collidepoint(event.pos):
                    button.click()
                    return True
            
            for i, button in enumerate(self.delete_buttons):
                if button.rect.collidepoint(event.pos):
                    button.click()
                    return True
        
        return False
    
    def load_game(self, filename):
        """
        Load the selected save game
        
        Args:
            filename: Save file to load
        """
        if self.game.save_manager.load_game(filename):
            # Change to playing state after successful load
            self.game.state_manager.change_state("playing")
    
    def delete_save(self, filename):
        """
        Delete the selected save file
        
        Args:
            filename: Save file to delete
        """
        try:
            save_path = os.path.join(self.game.save_manager.save_directory, filename)
            os.remove(save_path)
            # Refresh the save list
            self.refresh_save_list()
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error deleting save file: {e}")
    
    def draw(self):
        """Draw the load game panel"""
        # Calculate animated panel rect
        if self.animation_progress < 1:
            # Animate panel sliding down from top
            animated_height = int(self.panel_rect.height * self.animation_progress)
            animated_y = self.panel_rect.centery - animated_height // 2
            
            animated_rect = pygame.Rect(
                self.panel_rect.left,
                animated_y,
                self.panel_rect.width,
                animated_height
            )
        else:
            animated_rect = self.panel_rect
        
        # Draw panel background
        panel_surface = pygame.Surface((animated_rect.width, animated_rect.height), pygame.SRCALPHA)
        panel_surface.fill((30, 30, 50, 220))  # Semi-transparent dark blue
        
        # Draw scroll-like edges
        pygame.draw.rect(panel_surface, (80, 70, 60), 
                       (0, 0, animated_rect.width, animated_rect.height), 
                       scale_value(5))
        
        # Draw ornamental corners
        corner_size = scale_value(20)
        pygame.draw.rect(panel_surface, (100, 90, 70), 
                       (0, 0, corner_size, corner_size))
        pygame.draw.rect(panel_surface, (100, 90, 70), 
                       (animated_rect.width - corner_size, 0, corner_size, corner_size))
        pygame.draw.rect(panel_surface, (100, 90, 70), 
                       (0, animated_rect.height - corner_size, corner_size, corner_size))
        pygame.draw.rect(panel_surface, (100, 90, 70), 
                       (animated_rect.width - corner_size, animated_rect.height - corner_size, 
                        corner_size, corner_size))
        
        # Draw title
        title_surface = self.title_font.render("Load Game", True, (220, 220, 200))
        title_rect = title_surface.get_rect(midtop=(animated_rect.width // 2, scale_value(15)))
        panel_surface.blit(title_surface, title_rect)
        
        # Only draw save items if animation is complete
        if self.animation_progress == 1:
            if self.save_items:
                # Draw save items
                for item in self.save_items:
                    # Adjust rectangle position relative to panel
                    relative_rect = pygame.Rect(
                        item['rect'].left - self.panel_rect.left,
                        item['rect'].top - self.panel_rect.top,
                        item['rect'].width,
                        item['rect'].height
                    )
                    
                    # Draw item background
                    if item['selected']:
                        pygame.draw.rect(panel_surface, (60, 60, 80), relative_rect)
                    else:
                        pygame.draw.rect(panel_surface, (40, 40, 60), relative_rect)
                    
                    # Draw outline
                    pygame.draw.rect(panel_surface, (100, 100, 120), relative_rect, 1)
                    
                    # Draw save info
                    item_surface = self.item_font.render(item['display'], True, (220, 220, 220))
                    panel_surface.blit(item_surface, (
                        relative_rect.left + scale_value(10),
                        relative_rect.centery - item_surface.get_height() // 2
                    ))
                
                # Draw buttons on panel
                for button in self.load_buttons:
                    # Create a copy of the button with position relative to panel
                    panel_button = Button(
                        (button.rect.left - self.panel_rect.left, button.rect.top - self.panel_rect.top),
                        button.rect.size,
                        button.text,
                        None  # No callback needed for drawing
                    )
                    panel_button.hovered = button.hovered
                    panel_button.draw(panel_surface)
                
                for button in self.delete_buttons:
                    # Create a copy of the button with position relative to panel
                    panel_button = Button(
                        (button.rect.left - self.panel_rect.left, button.rect.top - self.panel_rect.top),
                        button.rect.size,
                        button.text,
                        None  # No callback needed for drawing
                    )
                    panel_button.hovered = button.hovered
                    panel_button.color = (150, 50, 50)  # Red for delete
                    panel_button.hover_color = (180, 60, 60)
                    panel_button.draw(panel_surface)
            else:
                # No saves available
                no_saves_surface = self.item_font.render("No save files found", True, (200, 200, 200))
                no_saves_rect = no_saves_surface.get_rect(center=(
                    animated_rect.width // 2,
                    animated_rect.height // 2
                ))
                panel_surface.blit(no_saves_surface, no_saves_rect)
        
        # Blit panel to screen
        self.screen.blit(panel_surface, animated_rect.topleft)