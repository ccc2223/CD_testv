# effects/particles.py
"""
Particle system for visual effects in Castle Defense
"""
import pygame
import random
import math
from utils import scale_value, scale_position

class Particle:
    """Base class for all particles"""
    def __init__(self, position, color, size, life, velocity=(0, 0), gravity=0):
        """
        Initialize particle with basic properties
        
        Args:
            position: Tuple of (x, y) starting coordinates
            color: RGB tuple color of the particle
            size: Initial size in pixels (will be scaled)
            life: Time in seconds the particle will exist
            velocity: Tuple of (vx, vy) initial velocity
            gravity: Downward acceleration to apply (0 for no gravity)
        """
        self.position = list(position)
        
        # Ensure color is valid - default to white if problems
        try:
            # Convert to int and clamp to 0-255 range
            r = max(0, min(255, int(color[0])))
            g = max(0, min(255, int(color[1])))
            b = max(0, min(255, int(color[2])))
            self.color = (r, g, b)
        except (IndexError, TypeError, ValueError):
            self.color = (255, 255, 255)  # Default to white
            
        self.size = scale_value(size)
        self.max_life = life
        self.life = life
        self.velocity = list(velocity)
        self.gravity = gravity
        self.alpha = 255  # Full opacity
        self.dead = False
    
    def update(self, dt):
        """
        Update particle state
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            False if particle is dead and should be removed
        """
        # Update life
        self.life -= dt
        if self.life <= 0:
            self.dead = True
            return False
        
        # Update position based on velocity
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        
        # Apply gravity
        self.velocity[1] += self.gravity * dt
        
        # Update alpha based on remaining life percentage
        life_pct = self.life / self.max_life
        self.alpha = int(255 * life_pct)
        
        return True
    
    def draw(self, screen):
        """
        Draw particle to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        if self.dead:
            return
            
        # Create a surface with per-pixel alpha
        size_int = max(1, int(self.size*2))
        particle_surface = pygame.Surface((size_int, size_int), pygame.SRCALPHA)
        
        # Get correct color values
        r, g, b = self.color
        a = self.alpha
        
        # Draw a circle using a simple technique
        color = (r, g, b, a)
        pos = (size_int // 2, size_int // 2)
        radius = max(1, int(self.size))
        
        pygame.draw.circle(particle_surface, color, pos, radius)
        
        # Blit to screen
        x = int(self.position[0] - self.size)
        y = int(self.position[1] - self.size)
        screen.blit(particle_surface, (x, y))

class ParticleSystem:
    """Manages multiple particles and their effects"""
    def __init__(self):
        """Initialize an empty particle system"""
        self.particles = []
    
    def update(self, dt):
        """
        Update all particles
        
        Args:
            dt: Time delta in seconds
        """
        # Update particles and remove dead ones
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, screen):
        """
        Draw all particles
        
        Args:
            screen: Pygame surface to draw on
        """
        for particle in self.particles:
            try:
                particle.draw(screen)
            except Exception as e:
                # Safely handle any drawing errors
                print(f"Error drawing particle: {e}")
                self.particles.remove(particle)
    
    def add_particle(self, particle):
        """
        Add a particle to the system
        
        Args:
            particle: Particle instance to add
        """
        self.particles.append(particle)
    
    def add_particles(self, particles):
        """
        Add multiple particles to the system
        
        Args:
            particles: List of Particle instances to add
        """
        self.particles.extend(particles)
    
    def is_empty(self):
        """
        Check if the particle system has any active particles
        
        Returns:
            True if no particles, False otherwise
        """
        return len(self.particles) == 0
    
    def clear(self):
        """Remove all particles from the system"""
        self.particles = []

class ProjectileParticle(Particle):
    """Particle that moves from source to target"""
    def __init__(self, start_pos, target_pos, color, size, life, speed):
        """
        Initialize projectile particle
        
        Args:
            start_pos: Tuple of (x, y) starting coordinates
            target_pos: Tuple of (x, y) target coordinates
            color: RGB tuple color of the particle
            size: Size in pixels
            life: Time in seconds the particle will exist
            speed: Speed in pixels per second
        """
        # Calculate direction and velocity
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize and scale by speed
            vx = (dx / distance) * speed
            vy = (dy / distance) * speed
        else:
            vx, vy = 0, 0
        
        super().__init__(start_pos, color, size, life, velocity=(vx, vy))
        self.target_pos = target_pos
        self.hit_target = False
        
        # Store original values for interpolation
        self.start_pos = list(start_pos)
        self.traveled = 0
        self.total_distance = distance
    
    def update(self, dt):
        """
        Update projectile position
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            False if projectile is dead and should be removed
        """
        if self.hit_target:
            self.dead = True
            return False
        
        # Calculate distance to target
        dx = self.target_pos[0] - self.position[0]
        dy = self.target_pos[1] - self.position[1]
        dist_to_target = math.sqrt(dx**2 + dy**2)
        
        # Check if we've reached or passed the target
        if dist_to_target < 5 or self.traveled >= self.total_distance:
            self.hit_target = True
            self.position[0] = self.target_pos[0]
            self.position[1] = self.target_pos[1]
            return False
        
        # Update position
        move_dist = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2) * dt
        self.traveled += move_dist
        
        # Standard update
        return super().update(dt)

class Animation:
    """Base class for complex animation effects"""
    def __init__(self, particle_system):
        """
        Initialize animation with a particle system
        
        Args:
            particle_system: ParticleSystem to add particles to
        """
        self.particle_system = particle_system
        self.completed = False
    
    def update(self, dt):
        """
        Update animation state
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            True if animation is still active, False if completed
        """
        return not self.completed
    
    def is_completed(self):
        """
        Check if animation is completed
        
        Returns:
            True if completed, False otherwise
        """
        return self.completed

# ---- Combat Animation Effects ----

def create_arrow_effect(start_pos, target_pos, particle_system, enhanced=False):
    """
    Create arrow projectile effect from tower to target
    
    Args:
        start_pos: Tuple of (x, y) starting coordinates (tower position)
        target_pos: Tuple of (x, y) target coordinates (monster position)
        particle_system: ParticleSystem to add particles to
        enhanced: Boolean indicating if this is an enhanced effect (for items)
    """
    # Create main arrow projectile
    arrow_color = (255, 130, 50) if enhanced else (200, 200, 200)
    arrow_size = 4 if enhanced else 3
    
    arrow = ProjectileParticle(
        start_pos,
        target_pos,
        arrow_color,
        arrow_size,
        0.5,  # Life in seconds
        scale_value(500 if enhanced else 450)  # Speed
    )
    
    # Add trail particles
    trail_count = 5 if enhanced else 3
    for _ in range(trail_count):
        offset_x = random.uniform(-5, 5)
        offset_y = random.uniform(-5, 5)
        
        # Enhanced trail with orange tint
        trail_color = (200, 150, 100) if enhanced else (150, 150, 150)
        
        trail = ProjectileParticle(
            (start_pos[0] + offset_x, start_pos[1] + offset_y),
            (target_pos[0] + offset_x, target_pos[1] + offset_y),
            trail_color,
            2,  # Smaller size
            0.3,  # Shorter life
            scale_value(400)  # Slightly slower
        )
        particle_system.add_particle(trail)
    
    particle_system.add_particle(arrow)

def create_sniper_shot_effect(start_pos, target_pos, particle_system, enhanced=False):
    """
    Create sniper shot effect with tracer line
    
    Args:
        start_pos: Tuple of (x, y) starting coordinates (tower position)
        target_pos: Tuple of (x, y) target coordinates (monster position)
        particle_system: ParticleSystem to add particles to
        enhanced: Boolean indicating if this is an enhanced effect (for items)
    """
    # Create high-speed projectile
    shot_color = (255, 100, 50) if enhanced else (255, 50, 50)
    shot_size = 3 if enhanced else 2
    
    shot = ProjectileParticle(
        start_pos,
        target_pos,
        shot_color,
        shot_size,
        0.2,  # Very short life
        scale_value(1200)  # Very fast
    )
    
    # Add tracer particles along line
    dx = target_pos[0] - start_pos[0]
    dy = target_pos[1] - start_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance > 0:
        # Create particles along the line
        num_particles = int(distance / (8 if enhanced else 10))
        for i in range(num_particles):
            # Position along the line
            t = i / num_particles
            pos_x = start_pos[0] + dx * t
            pos_y = start_pos[1] + dy * t
            
            # Add small stationary particle with random offset
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            
            # Enhanced tracer with orange tint
            tracer_color = (255, 150, 100) if enhanced else (255, 100, 100)
            
            tracer = Particle(
                (pos_x + offset_x, pos_y + offset_y),
                tracer_color,
                1,  # Small size
                0.3 + random.uniform(0, 0.2)  # Random life
            )
            particle_system.add_particle(tracer)
    
    particle_system.add_particle(shot)

def create_splash_effect(position, radius, particle_system, enhanced=False):
    """
    Create explosion effect at target position
    
    Args:
        position: Tuple of (x, y) coordinates of explosion center
        radius: Radius of explosion effect
        particle_system: ParticleSystem to add particles to
        enhanced: Boolean indicating if this is an enhanced effect (for items)
    """
    # Scale the radius
    scaled_radius = scale_value(radius)
    
    # More particles for enhanced effect
    num_particles = int(scaled_radius * (1.2 if enhanced else 0.8))
    
    # Add explosion particles in circle
    for _ in range(num_particles):
        # Random angle and distance from center
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(0, scaled_radius)
        
        # Position with offset
        pos_x = position[0] + math.cos(angle) * distance
        pos_y = position[1] + math.sin(angle) * distance
        
        # Velocity away from center - faster for enhanced
        speed_factor = 1.3 if enhanced else 1.0
        vel_x = math.cos(angle) * scale_value(random.uniform(20, 80) * speed_factor)
        vel_y = math.sin(angle) * scale_value(random.uniform(20, 80) * speed_factor)
        
        # Random orange/red/yellow color for explosion - brighter for enhanced
        if enhanced:
            r = random.randint(230, 255)
            g = random.randint(100, 180)
            b = random.randint(50, 100)
        else:
            r = random.randint(200, 255)
            g = random.randint(50, 150)
            b = random.randint(0, 50)
        
        # Create particle with outward velocity
        particle = Particle(
            (pos_x, pos_y),
            (r, g, b),
            random.uniform(2, 5 if enhanced else 4),
            random.uniform(0.3, 0.8 if enhanced else 0.6),
            velocity=(vel_x, vel_y)
        )
        particle_system.add_particle(particle)

def create_freeze_effect(position, radius, particle_system, enhanced=False):
    """
    Create freeze effect around tower or at target
    
    Args:
        position: Tuple of (x, y) coordinates of freeze center
        radius: Radius of freeze effect
        particle_system: ParticleSystem to add particles to
        enhanced: Boolean indicating if this is an enhanced effect (for items)
    """
    # Scale the radius
    scaled_radius = scale_value(radius)
    
    # More particles for enhanced effect
    num_particles = int(scaled_radius * (1.0 if enhanced else 0.6))
    
    # Create frost particles in expanding circle
    for _ in range(num_particles):
        # Random angle and distance from center
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(0, scaled_radius)
        
        # Position with offset
        pos_x = position[0] + math.cos(angle) * distance
        pos_y = position[1] + math.sin(angle) * distance
        
        # Slow outward velocity - slightly faster for enhanced
        speed_factor = 1.2 if enhanced else 1.0
        vel_x = math.cos(angle) * scale_value(random.uniform(5, 20) * speed_factor)
        vel_y = math.sin(angle) * scale_value(random.uniform(5, 20) * speed_factor)
        
        # Blue/cyan color for ice - more vibrant for enhanced
        if enhanced:
            r = random.randint(50, 100)
            g = random.randint(180, 255)
            b = random.randint(230, 255)
        else:
            r = random.randint(100, 150)
            g = random.randint(200, 255)
            b = random.randint(220, 255)
        
        # Create particle with slow outward velocity
        particle = Particle(
            (pos_x, pos_y),
            (r, g, b),
            random.uniform(1, 4 if enhanced else 3),
            random.uniform(0.5, 1.5 if enhanced else 1.2),
            velocity=(vel_x, vel_y)
        )
        particle_system.add_particle(particle)
        
        # Add extra "ice crystal" particles for enhanced effect
        if enhanced and random.random() < 0.3:
            crystal = Particle(
                (pos_x, pos_y),
                (200, 240, 255),
                random.uniform(1, 2),
                random.uniform(0.8, 1.5),
                velocity=(vel_x * 0.5, vel_y * 0.5)
            )
            particle_system.add_particle(crystal)

def create_monster_hit_effect(position, particle_system, color=(255, 0, 0)):
    """
    Create impact effect when monster is hit
    
    Args:
        position: Tuple of (x, y) coordinates of monster center
        particle_system: ParticleSystem to add particles to
        color: Base color for the hit effect (default: red)
    """
    # Number of particles
    num_particles = random.randint(5, 10)
    
    # Create particles in small burst
    for _ in range(num_particles):
        # Random angle and velocity
        angle = random.uniform(0, math.pi * 2)
        speed = scale_value(random.uniform(30, 80))
        
        # Velocity based on angle and speed
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        
        # Variation on the base color
        r = min(255, color[0] + random.randint(-20, 20))
        g = min(255, color[1] + random.randint(-20, 20))
        b = min(255, color[2] + random.randint(-20, 20))
        
        # Create particle with outward velocity and gravity
        particle = Particle(
            position,
            (r, g, b),
            random.uniform(1, 3),
            random.uniform(0.2, 0.5),
            velocity=(vel_x, vel_y),
            gravity=scale_value(100)
        )
        particle_system.add_particle(particle)

def create_monster_death_effect(position, monster_size, particle_system, monster_color):
    """
    Create death effect when monster is killed
    
    Args:
        position: Tuple of (x, y) coordinates of monster center
        monster_size: Size of the monster for scaling effect
        particle_system: ParticleSystem to add particles to
        monster_color: Base color of the monster
    """
    # Number of particles based on monster size
    scaled_size = scale_value(monster_size)
    num_particles = int(scaled_size * 2)
    
    # Create particles for disintegration effect
    for _ in range(num_particles):
        # Random position within monster bounds
        offset_x = random.uniform(-scaled_size/2, scaled_size/2)
        offset_y = random.uniform(-scaled_size/2, scaled_size/2)
        pos = (position[0] + offset_x, position[1] + offset_y)
        
        # Random angle and velocity for explosion
        angle = random.uniform(0, math.pi * 2)
        speed = scale_value(random.uniform(20, 100))
        
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        
        # Base on monster color but add variation
        r = min(255, monster_color[0] + random.randint(-30, 30))
        g = min(255, monster_color[1] + random.randint(-30, 30))
        b = min(255, monster_color[2] + random.randint(-30, 30))
        
        # Create particle with outward velocity and gravity
        particle = Particle(
            pos,
            (r, g, b),
            random.uniform(1, 4),
            random.uniform(0.5, 1.0),
            velocity=(vel_x, vel_y),
            gravity=scale_value(150)
        )
        particle_system.add_particle(particle)

def create_slow_effect_particles(position, particle_system):
    """
    Create particles indicating monster is slowed
    
    Args:
        position: Tuple of (x, y) coordinates of monster center
        particle_system: ParticleSystem to add particles to
    """
    # Create occasional frost particles above the monster
    if random.random() < 0.7:  # 70% chance each frame
        # Random position near monster
        offset_x = random.uniform(-10, 10)
        offset_y = random.uniform(-15, -5)  # Above monster
        pos = (position[0] + offset_x, position[1] + offset_y)
        
        # Slow upward drift
        vel_y = scale_value(random.uniform(-15, -5))
        
        # Ice blue color
        r = random.randint(180, 220)
        g = random.randint(220, 255)
        b = 255
        
        # Create drifting ice particle
        particle = Particle(
            pos,
            (r, g, b),
            random.uniform(1, 2),
            random.uniform(0.3, 0.8),
            velocity=(0, vel_y)
        )
        particle_system.add_particle(particle)

# NEW: Castle attack effect
def create_castle_attack_effect(monster_pos, castle_pos, particle_system, monster_color):
    """
    Create effect for monster attacking castle
    
    Args:
        monster_pos: Tuple of (x, y) coordinates of monster
        castle_pos: Tuple of (x, y) coordinates on castle being attacked
        particle_system: ParticleSystem to add particles to
        monster_color: Base color of the monster for particles
    """
    # Calculate direction from monster to castle
    dx = castle_pos[0] - monster_pos[0]
    dy = castle_pos[1] - monster_pos[1]
    angle = math.atan2(dy, dx)
    
    # Create a small burst of 'impact' particles at the castle
    num_particles = random.randint(8, 15)
    
    # Make particles more visible by enhancing color
    r = min(255, monster_color[0] + 50)
    g = min(255, monster_color[1] + 30)
    b = min(255, monster_color[2] + 30)
    enhanced_color = (r, g, b)
    
    # Calculate position slightly away from castle wall to make the effect more visible
    impact_distance = scale_value(5)
    impact_pos = (
        castle_pos[0] - math.cos(angle) * impact_distance,
        castle_pos[1] - math.sin(angle) * impact_distance
    )
    
    # Create impact particles
    for _ in range(num_particles):
        # Calculate spread angle (mostly away from castle)
        spread_angle = angle + math.pi + random.uniform(-0.8, 0.8)
        
        # Velocity based on spread angle
        speed = scale_value(random.uniform(30, 100))
        vel_x = math.cos(spread_angle) * speed
        vel_y = math.sin(spread_angle) * speed
        
        # Slight variation in color
        color_variation = random.randint(-20, 20)
        particle_color = (
            max(0, min(255, enhanced_color[0] + color_variation)),
            max(0, min(255, enhanced_color[1] + color_variation)),
            max(0, min(255, enhanced_color[2] + color_variation))
        )
        
        # Create impact particle
        particle = Particle(
            impact_pos,
            particle_color,
            random.uniform(1.5, 3.5),
            random.uniform(0.2, 0.4),
            velocity=(vel_x, vel_y),
            gravity=scale_value(200)
        )
        particle_system.add_particle(particle)
    
    # Create a few projectile trails from monster to castle
    num_trails = random.randint(1, 3)
    for _ in range(num_trails):
        # Create small offset for variation
        offset_x = random.uniform(-10, 10)
        offset_y = random.uniform(-10, 10)
        start_pos = (monster_pos[0] + offset_x, monster_pos[1] + offset_y)
        end_pos = (castle_pos[0] + offset_x/2, castle_pos[1] + offset_y/2)
        
        # Create projectile with monster's color
        projectile = ProjectileParticle(
            start_pos,
            end_pos,
            enhanced_color,
            random.uniform(1.5, 2.5),
            0.15,  # Short life for quick attack
            scale_value(600)  # Fast speed
        )
        particle_system.add_particle(projectile)
