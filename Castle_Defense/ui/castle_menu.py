# ui/castle_menu.py
"""
Castle upgrade menu UI for Castle Defense
"""
import pygame
from ui.menus import Menu, Button
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class CastleMenu(Menu):
    """Menu for upgrading the castle"""
    def __init__(self, screen):
        """
        Initialize castle menu
        
        Args:
            screen: Pygame surface to draw on
        """
        super().__init__(screen)
        self.castle = None
        self.resource_manager = None
        self.title = "Castle Upgrades"
        
        # Position on left side instead of right
        self.position = (20, 100)
        self.size = (280, 400)
        self.rect = pygame.Rect(self.position, self.size)
    
    def set_castle(self, castle, resource_manager):
        """
        Set the castle this menu controls
        
        Args:
            castle: Castle instance
            resource_manager: ResourceManager for resources
        """
        self.castle = castle
        self.resource_manager = resource_manager
        
        # Clear existing buttons
        self.buttons = []
        
        # Create upgrade buttons
        button_width = self.rect.width - 40
        y_pos = self.rect.top + 50
        
        # Health upgrade button
        health_cost = castle.get_health_upgrade_cost()
        can_upgrade_health = resource_manager.has_resources(health_cost)
        
        health_button = Button(
            (self.rect.left + 20, y_pos),
            (button_width, 40),
            f"Upgrade Castle Walls",
            self.upgrade_castle_health
        )
        health_button.set_disabled(not can_upgrade_health)
        self.buttons.append(health_button)
        
        # Damage reduction upgrade button
        dr_cost = castle.get_damage_reduction_upgrade_cost()
        can_upgrade_dr = resource_manager.has_resources(dr_cost)
        
        dr_button = Button(
            (self.rect.left + 20, y_pos + 100),
            (button_width, 40),
            f"Upgrade Damage Reduction",
            self.upgrade_castle_damage_reduction
        )
        dr_button.set_disabled(not can_upgrade_dr)
        self.buttons.append(dr_button)
        
        # Health regen upgrade button
        regen_cost = castle.get_health_regen_upgrade_cost()
        can_upgrade_regen = resource_manager.has_resources(regen_cost)
        
        regen_button = Button(
            (self.rect.left + 20, y_pos + 200),
            (button_width, 40),
            f"Upgrade Health Regeneration",
            self.upgrade_castle_health_regen
        )
        regen_button.set_disabled(not can_upgrade_regen)
        self.buttons.append(regen_button)
    
    def upgrade_castle_health(self):
        """Upgrade castle health"""
        if self.castle and self.resource_manager:
            if self.castle.upgrade_health(self.resource_manager):
                # Refresh the menu to update costs and button states
                self.set_castle(self.castle, self.resource_manager)
    
    def upgrade_castle_damage_reduction(self):
        """Upgrade castle damage reduction"""
        if self.castle and self.resource_manager:
            if self.castle.upgrade_damage_reduction(self.resource_manager):
                # Refresh the menu to update costs and button states
                self.set_castle(self.castle, self.resource_manager)
    
    def upgrade_castle_health_regen(self):
        """Upgrade castle health regeneration"""
        if self.castle and self.resource_manager:
            if self.castle.upgrade_health_regen(self.resource_manager):
                # Refresh the menu to update costs and button states
                self.set_castle(self.castle, self.resource_manager)
    
    def update_button_states(self):
        """Update button enabled/disabled states based on available resources"""
        if not self.castle or not self.resource_manager:
            return
        
        # Update health upgrade button
        health_cost = self.castle.get_health_upgrade_cost()
        can_upgrade_health = self.resource_manager.has_resources(health_cost)
        self.buttons[0].set_disabled(not can_upgrade_health)
        
        # Update damage reduction upgrade button
        dr_cost = self.castle.get_damage_reduction_upgrade_cost()
        can_upgrade_dr = self.resource_manager.has_resources(dr_cost)
        self.buttons[1].set_disabled(not can_upgrade_dr)
        
        # Update health regen upgrade button
        regen_cost = self.castle.get_health_regen_upgrade_cost()
        can_upgrade_regen = self.resource_manager.has_resources(regen_cost)
        self.buttons[2].set_disabled(not can_upgrade_regen)
    
    def draw(self):
        """Draw castle menu with upgrade options"""
        super().draw()
        
        if not self.active or not self.castle:
            return
        
        # Update button states
        self.update_button_states()
        
        # Draw castle stats
        y_pos = self.rect.top + 60
        
        # Draw health upgrade info
        self.draw_upgrade_section(
            y_pos + 35,
            f"Wall Strength (Lv {self.castle.health_upgrade_level})",
            f"Current HP: {int(self.castle.health)}/{int(self.castle.max_health)}",
            f"Next: {int(self.castle.max_health * 1.5)} HP",
            self.castle.get_health_upgrade_cost()
        )
        
        # Draw damage reduction upgrade info
        damage_reduction_pct = int(self.castle.damage_reduction * 100)
        next_dr_pct = int(min(0.9, self.castle.damage_reduction * 1.2) * 100)
        
        self.draw_upgrade_section(
            y_pos + 135,
            f"Armor (Lv {self.castle.damage_reduction_upgrade_level})",
            f"Reduction: {damage_reduction_pct}%",
            f"Next: {next_dr_pct}%",
            self.castle.get_damage_reduction_upgrade_cost()
        )
        
        # Draw health regen upgrade info
        next_regen = self.castle.health_regen * 1.3
        
        self.draw_upgrade_section(
            y_pos + 235,
            f"Repair (Lv {self.castle.health_regen_upgrade_level})",
            f"Regen: {self.castle.health_regen:.1f} HP/s",
            f"Next: {next_regen:.1f} HP/s",
            self.castle.get_health_regen_upgrade_cost()
        )
    
    def draw_upgrade_section(self, y_pos, title, current, next_level, cost):
        """
        Draw an upgrade section with title, stats, and cost
        
        Args:
            y_pos: Y position to start drawing
            title: Section title
            current: Current stat text
            next_level: Next level stat text
            cost: Dictionary of costs
        """
        # Draw section title
        title_font = pygame.font.Font(None, 20)
        title_surface = title_font.render(title, True, (255, 255, 200))
        self.screen.blit(title_surface, (self.rect.left + 20, y_pos))
        
        # Draw current stat
        y_pos += 20
        stat_font = pygame.font.Font(None, 18)
        current_surface = stat_font.render(current, True, (200, 200, 255))
        self.screen.blit(current_surface, (self.rect.left + 30, y_pos))
        
        # Draw next level stat
        y_pos += 18
        next_surface = stat_font.render(next_level, True, (150, 255, 150))
        self.screen.blit(next_surface, (self.rect.left + 30, y_pos))
        
        # Draw cost
        y_pos += 25
        # Check if we have enough resources
        has_resources = self.resource_manager.has_resources(cost)
        cost_color = (100, 255, 100) if has_resources else (255, 100, 100)
        
        cost_text = "Cost: " + ", ".join(f"{amt} {res}" for res, amt in cost.items())
        cost_surface = stat_font.render(cost_text, True, cost_color)
        self.screen.blit(cost_surface, (self.rect.left + 25, y_pos))
