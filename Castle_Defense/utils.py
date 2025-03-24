# utils.py
"""
Utility functions for the Castle Defense game
"""
import math
import pygame
from config import SCALE_X, SCALE_Y, REF_WIDTH, REF_HEIGHT

def distance(pos1, pos2):
    """
    Calculate Euclidean distance between two points
    
    Args:
        pos1: Tuple of (x, y) coordinates
        pos2: Tuple of (x, y) coordinates
        
    Returns:
        Float distance between points
    """
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

def normalize(vector):
    """
    Normalize a vector to unit length
    
    Args:
        vector: Tuple of (x, y) vector components
        
    Returns:
        Normalized vector as (x, y) tuple
    """
    length = math.sqrt(vector[0]**2 + vector[1]**2)
    if length == 0:
        return (0, 0)
    return (vector[0] / length, vector[1] / length)

def calculate_angle(pos1, pos2):
    """
    Calculate angle in radians between two points
    
    Args:
        pos1: Tuple of (x, y) coordinates (origin)
        pos2: Tuple of (x, y) coordinates (target)
        
    Returns:
        Angle in radians
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.atan2(dy, dx)

def draw_health_bar(surface, position, size, value, max_value, color=(0, 255, 0), bg_color=(255, 0, 0)):
    """
    Draw a health bar
    
    Args:
        surface: Pygame surface to draw on
        position: Tuple of (x, y) position of top-left corner
        size: Tuple of (width, height) of the bar
        value: Current health value
        max_value: Maximum health value
        color: RGB color for health (default: green)
        bg_color: RGB color for background (default: red)
    """
    # Ensure value doesn't exceed max
    ratio = min(value / max_value, 1.0)
    
    # Draw background
    pygame.draw.rect(surface, bg_color, (*position, *size))
    
    # Draw health
    if ratio > 0:
        pygame.draw.rect(surface, color, 
                         (position[0], position[1], int(size[0] * ratio), size[1]))
    
    # Draw border
    pygame.draw.rect(surface, (0, 0, 0), (*position, *size), 1)

def scale_position(pos):
    """
    Scale a position from reference dimensions to current window size
    
    Args:
        pos: Tuple of (x, y) coordinates in reference dimensions
        
    Returns:
        Tuple of scaled (x, y) coordinates
    """
    return (int(pos[0] * SCALE_X), int(pos[1] * SCALE_Y))

def scale_size(size):
    """
    Scale a size from reference dimensions to current window size
    
    Args:
        size: Tuple of (width, height) in reference dimensions
        
    Returns:
        Tuple of scaled (width, height)
    """
    return (int(size[0] * SCALE_X), int(size[1] * SCALE_Y))

def scale_value(value):
    """
    Scale a single value (like radius, font size, etc.)
    
    Args:
        value: Value to scale
        
    Returns:
        Scaled value
    """
    # Use average of X and Y scale for uniform scaling
    scale_factor = (SCALE_X + SCALE_Y) / 2
    return int(value * scale_factor)

def unscale_position(pos):
    """
    Convert a position from screen coordinates to reference coordinates
    
    Args:
        pos: Tuple of (x, y) coordinates in screen dimensions
        
    Returns:
        Tuple of (x, y) coordinates in reference dimensions
    """
    return (int(pos[0] / SCALE_X), int(pos[1] / SCALE_Y))
