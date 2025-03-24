# ui/dev_menu/components.py
"""
UI components for the developer menu
"""
import pygame
import math

class Button:
    """Button control for the developer menu"""
    def __init__(self, position, size, text, callback, color=(80, 80, 80)):
        """
        Initialize button
        
        Args:
            position: Tuple of (x, y) coordinates
            size: Tuple of (width, height)
            text: Button text
            callback: Function to call when clicked
            color: RGB color tuple for button
        """
        self.position = position
        self.size = size
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = (100, 100, 100)
        self.rect = pygame.Rect(position, size)
        self.hovered = False
        self.font = pygame.font.Font(None, 18)
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:  # Left click
                if self.callback:
                    self.callback()
                return True
        
        return False
    
    def draw(self, screen):
        """Draw the button"""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 1)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
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
            width: Width of the slider
            label: Text label
            value: Initial value
            min_value: Minimum value
            max_value: Maximum value
            step: Step size for increments
            callback: Function to call when value changes
            format_func: Function to format displayed value
        """
        self.position = position
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
            width - self.label_width - self.value_width,
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
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.handle_rect.collidepoint(event.pos):
                    self.dragging = True
                    return True
                elif self.slider_rect.collidepoint(event.pos):
                    # Click on slider bar - move handle to that position
                    self.set_value_from_mouse_x(event.pos[0])
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.set_value_from_mouse_x(event.pos[0])
                return True
        
        return False
    
    def set_value_from_mouse_x(self, mouse_x):
        """Calculate and set value based on mouse x position"""
        slider_width = self.slider_rect.width
        if slider_width == 0:
            return  # Avoid division by zero
            
        # Calculate relative position in slider (0.0 to 1.0)
        relative_pos = max(0, min(1, (mouse_x - self.slider_rect.left) / slider_width))
        
        # Calculate value
        new_value = self.min_value + relative_pos * (self.max_value - self.min_value)
        
        # Round to nearest step
        new_value = round(new_value / self.step) * self.step
        
        # Clamp to range
        new_value = max(self.min_value, min(self.max_value, new_value))
        
        # Only update if value has changed
        if new_value != self.value:
            self.value = new_value
            if self.callback:
                self.callback(self.value)
            self.update_handle()
    
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


class Checkbox:
    """Checkbox control for toggling boolean values"""
    def __init__(self, position, label, checked=False, callback=None):
        """
        Initialize checkbox
        
        Args:
            position: Tuple of (x, y) coordinates
            label: Text label
            checked: Initial checked state
            callback: Function to call when state changes
        """
        self.position = position
        self.label = label
        self.checked = checked
        self.callback = callback
        
        self.box_size = 16
        self.box_rect = pygame.Rect(position[0], position[1], self.box_size, self.box_size)
        self.font = pygame.font.Font(None, 18)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.box_rect.collidepoint(event.pos):  # Left click
                self.checked = not self.checked
                if self.callback:
                    self.callback(self.checked)
                return True
        
        return False
    
    def draw(self, screen):
        """Draw the checkbox"""
        # Draw box
        pygame.draw.rect(screen, (60, 60, 60), self.box_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.box_rect, 1)
        
        # Draw check mark if checked
        if self.checked:
            inner_rect = pygame.Rect(
                self.box_rect.left + 3,
                self.box_rect.top + 3,
                self.box_rect.width - 6,
                self.box_rect.height - 6
            )
            pygame.draw.rect(screen, (150, 250, 150), inner_rect)
        
        # Draw label
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.box_rect.right + 5, self.box_rect.top))


class TextInput:
    """Text input control for entering values"""
    def __init__(self, position, width, label, initial_text="", callback=None):
        """
        Initialize text input
        
        Args:
            position: Tuple of (x, y) coordinates
            width: Width of the input field
            label: Text label
            initial_text: Initial text value
            callback: Function to call when value changes
        """
        self.position = position
        self.width = width
        self.height = 20
        self.label = label
        self.text = initial_text
        self.callback = callback
        
        self.label_width = 180
        self.input_rect = pygame.Rect(
            position[0] + self.label_width,
            position[1],
            width - self.label_width,
            self.height
        )
        
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
        self.font = pygame.font.Font(None, 18)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Toggle active state
                self.active = self.input_rect.collidepoint(event.pos)
                return self.active
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                if self.callback:
                    self.callback(self.text)
            
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            
            else:
                # Only add valid characters
                if event.unicode.isdigit() or event.unicode == '.':
                    self.text += event.unicode
            
            return True
        
        return False
    
    def update(self, dt):
        """Update cursor blinking"""
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:  # Blink every 0.5 seconds
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        """Draw the text input"""
        # Draw label
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.position[0], self.position[1] + 2))
        
        # Draw input background
        if self.active:
            bg_color = (80, 80, 100)
        else:
            bg_color = (60, 60, 60)
        
        pygame.draw.rect(screen, bg_color, self.input_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.input_rect, 1)
        
        # Draw text
        if self.text:
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midleft=(self.input_rect.left + 5, self.input_rect.centery))
            screen.blit(text_surface, text_rect)
        
        # Draw cursor
        if self.active and self.cursor_visible:
            if self.text:
                text_width = self.font.size(self.text)[0]
                cursor_x = self.input_rect.left + 5 + text_width
            else:
                cursor_x = self.input_rect.left + 5
            
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (cursor_x, self.input_rect.top + 3),
                (cursor_x, self.input_rect.bottom - 3),
                1
            )


class DropdownMenu:
    """Dropdown menu for selecting from a list of options"""
    def __init__(self, position, width, label, options, selected_index=0, callback=None):
        """
        Initialize dropdown menu
        
        Args:
            position: Tuple of (x, y) coordinates
            width: Width of the dropdown
            label: Text label
            options: List of option strings
            selected_index: Initial selected index
            callback: Function to call when selection changes
        """
        self.position = position
        self.width = width
        self.height = 20
        self.label = label
        self.options = options
        self.selected_index = selected_index
        self.callback = callback
        
        self.label_width = 180
        self.dropdown_rect = pygame.Rect(
            position[0] + self.label_width,
            position[1],
            width - self.label_width,
            self.height
        )
        
        self.max_options_visible = 5
        self.option_height = 20
        
        self.expanded = False
        self.hover_index = -1
        
        self.font = pygame.font.Font(None, 18)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Returns:
            True if event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.dropdown_rect.collidepoint(event.pos):
                    self.expanded = not self.expanded
                    return True
                
                elif self.expanded:
                    # Check if clicking on an option
                    for i in range(min(len(self.options), self.max_options_visible)):
                        option_rect = pygame.Rect(
                            self.dropdown_rect.left,
                            self.dropdown_rect.bottom + i * self.option_height,
                            self.dropdown_rect.width,
                            self.option_height
                        )
                        
                        if option_rect.collidepoint(event.pos):
                            self.selected_index = i
                            self.expanded = False
                            if self.callback:
                                self.callback(self.selected_index)
                            return True
                    
                    # Clicking outside the dropdown closes it
                    self.expanded = False
                    return True
        
        elif event.type == pygame.MOUSEMOTION and self.expanded:
            # Check for hover over options
            self.hover_index = -1
            for i in range(min(len(self.options), self.max_options_visible)):
                option_rect = pygame.Rect(
                    self.dropdown_rect.left,
                    self.dropdown_rect.bottom + i * self.option_height,
                    self.dropdown_rect.width,
                    self.option_height
                )
                
                if option_rect.collidepoint(event.pos):
                    self.hover_index = i
                    return True
        
        return False
    
    def update(self, mouse_pos):
        """Update dropdown hover states based on mouse position"""
        self.hover_index = -1
        # Check if mouse is over the dropdown
        if self.expanded:
            for i in range(min(len(self.options), self.max_options_visible)):
                option_rect = pygame.Rect(
                    self.dropdown_rect.left,
                    self.dropdown_rect.bottom + i * self.option_height,
                    self.dropdown_rect.width,
                    self.option_height
                )
                
                if option_rect.collidepoint(mouse_pos):
                    self.hover_index = i
                    break
    
    def draw(self, screen):
        """Draw the dropdown menu"""
        # Draw label
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.position[0], self.position[1] + 2))
        
        # Draw dropdown background
        pygame.draw.rect(screen, (60, 60, 60), self.dropdown_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.dropdown_rect, 1)
        
        # Draw selected option
        if 0 <= self.selected_index < len(self.options):
            selected_text = self.options[self.selected_index]
            text_surface = self.font.render(selected_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midleft=(self.dropdown_rect.left + 5, self.dropdown_rect.centery))
            screen.blit(text_surface, text_rect)
        
        # Draw dropdown arrow
        arrow_points = [
            (self.dropdown_rect.right - 15, self.dropdown_rect.centery - 3),
            (self.dropdown_rect.right - 5, self.dropdown_rect.centery - 3),
            (self.dropdown_rect.right - 10, self.dropdown_rect.centery + 3)
        ]
        pygame.draw.polygon(screen, (200, 200, 200), arrow_points)
        
        # Draw expanded options
        if self.expanded:
            for i in range(min(len(self.options), self.max_options_visible)):
                option_rect = pygame.Rect(
                    self.dropdown_rect.left,
                    self.dropdown_rect.bottom + i * self.option_height,
                    self.dropdown_rect.width,
                    self.option_height
                )
                
                if i == self.hover_index:
                    bg_color = (100, 100, 120)
                else:
                    bg_color = (80, 80, 90)
                
                pygame.draw.rect(screen, bg_color, option_rect)
                pygame.draw.rect(screen, (150, 150, 150), option_rect, 1)
                
                option_text = self.options[i]
                text_surface = self.font.render(option_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(midleft=(option_rect.left + 5, option_rect.centery))
                screen.blit(text_surface, text_rect)


class TabButton:
    """Button for switching tabs in the developer menu"""
    def __init__(self, position, width, text, tab_id):
        """
        Initialize tab button
        
        Args:
            position: Tuple of (x, y) coordinates
            width: Width of the button
            text: Button text
            tab_id: ID of the tab this button should activate
        """
        self.position = position
        self.width = width
        self.height = 30
        self.text = text
        self.tab_id = tab_id
        self.rect = pygame.Rect(position[0], position[1], width, self.height)
        self.active = False
        self.hovered = False
        self.font = pygame.font.Font(None, 20)
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen):
        """Draw the tab button"""
        if self.active:
            color = (150, 200, 150)
        elif self.hovered:
            color = (100, 150, 100)
        else:
            color = (80, 80, 80)
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 1)
        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Tab:
    """Base class for developer menu tabs"""
    def __init__(self, rect):
        """
        Initialize tab
        
        Args:
            rect: Pygame Rect defining the tab area
        """
        self.rect = rect
        self.controls = []
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 24)
    
    def handle_event(self, event):
        """
        Handle events for all controls in the tab
        
        Returns:
            True if any control handled the event, False otherwise
        """
        handled = False
        for control in self.controls:
            if control.handle_event(event):
                handled = True
        return handled
    
    def update(self, dt):
        """Update all controls that need updating"""
        # Get current mouse position for controls that need it
        mouse_pos = pygame.mouse.get_pos()
        
        for control in self.controls:
            if hasattr(control, 'update'):
                if isinstance(control, (Button, TabButton, Checkbox, DropdownMenu)):
                    # These controls need mouse position
                    control.update(mouse_pos)
                else:
                    # Other controls (like TextInput) need delta time
                    control.update(dt)
    
    def draw(self, screen):
        """Draw the tab and all its controls"""
        # Draw tab background
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        
        # Draw controls
        for control in self.controls:
            control.draw(screen)
