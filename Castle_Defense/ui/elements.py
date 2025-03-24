# ui/elements.py
"""
Basic UI elements for Castle Defense
"""
import pygame

class Button:
    """Interactive button for menus"""
    def __init__(self, position, size, text, callback, color=(100, 100, 100), 
                 hover_color=(150, 150, 150), text_color=(255, 255, 255), 
                 disabled_color=(60, 60, 60), disabled=False):
        """
        Initialize button
        
        Args:
            position: Tuple of (x, y) coordinates
            size: Tuple of (width, height)
            text: Button text
            callback: Function to call when clicked
            color: RGB color tuple for button
            hover_color: RGB color tuple for button when hovered
            text_color: RGB color tuple for text
            disabled_color: RGB color tuple for disabled button
            disabled: Boolean indicating if button is disabled
        """
        self.position = position
        self.size = size
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.disabled_color = disabled_color
        self.rect = pygame.Rect(position, size)
        self.hovered = False
        self.disabled = disabled
        self.font = pygame.font.Font(None, 20)
    
    def update(self, mouse_pos):
        """
        Update button state based on mouse position
        
        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates
        """
        if not self.disabled:
            self.hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.hovered = False
    
    def click(self):
        """Execute button callback when clicked"""
        if self.callback and not self.disabled:
            self.callback()
    
    def set_disabled(self, disabled):
        """
        Set button disabled state
        
        Args:
            disabled: Boolean indicating if button should be disabled
        """
        self.disabled = disabled
    
    def draw(self, screen):
        """
        Draw button to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw button background
        if self.disabled:
            color = self.disabled_color
        else:
            color = self.hover_color if self.hovered else self.color
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        
        # Draw button text
        text_color = (150, 150, 150) if self.disabled else self.text_color
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Slider:
    """Slider control for adjusting numeric values"""
    def __init__(self, position, width, label, value, min_value, max_value, step=0.1, 
                 callback=None, format_func=None):
        """
        Initialize slider
        
        Args:
            position: Tuple of (x, y) coordinates
            width: Width of the slider (int) or size tuple (width, height)
            label: Text label
            value: Initial value
            min_value: Minimum value
            max_value: Maximum value
            step: Step size for increments
            callback: Function to call when value changes
            format_func: Function to format displayed value
        """
        self.position = position
        
        # Handle case where width is a tuple (width, height)
        if isinstance(width, tuple):
            self.width = width[0]
            self.height = width[1]
        else:
            self.width = width
            self.height = 20
            
        self.label = label
        self.value = value
        self.original_value = value  # Store original for reset
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.callback = callback
        self.format_func = format_func or (lambda x: f"{x:.2f}")
        
        self.label_width = 180
        self.value_width = 60
        
        # Calculate slider rect
        self.slider_rect = pygame.Rect(
            position[0] + self.label_width,
            position[1],
            self.width - self.label_width - self.value_width,
            self.height
        )
        
        # Calculate handle position
        self.update_handle()
        
        self.dragging = False
        self.font = pygame.font.Font(None, 18)
    
    def update_handle(self):
        """Update the position of the slider handle based on value"""
        value_range = self.max_value - self.min_value
        if value_range == 0:
            value_range = 1  # Avoid division by zero
        
        value_ratio = (self.value - self.min_value) / value_range
        handle_x = self.slider_rect.left + int(value_ratio * self.slider_rect.width)
        
        self.handle_rect = pygame.Rect(
            handle_x - 5,
            self.slider_rect.top - 5,
            10,
            self.slider_rect.height + 10
        )
    
    def reset(self):
        """Reset to original value"""
        self.value = self.original_value
        self.update_handle()
        if self.callback:
            self.callback(self.value)
    
    def draw(self, screen):
        """Draw the slider"""
        # Draw label
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.position[0], self.position[1] + 2))
        
        # Draw slider background
        pygame.draw.rect(screen, (60, 60, 60), self.slider_rect)
        pygame.draw.rect(screen, (120, 120, 120), self.slider_rect, 1)
        
        # Draw handle
        if self.dragging:
            handle_color = (200, 200, 100)
        else:
            handle_color = (150, 150, 150)
        pygame.draw.rect(screen, handle_color, self.handle_rect)
        
        # Draw value
        value_text = self.format_func(self.value)
        value_surface = self.font.render(value_text, True, (255, 255, 255))
        value_rect = value_surface.get_rect(
            midleft=(self.slider_rect.right + 10, self.slider_rect.centery)
        )
        screen.blit(value_surface, value_rect)
