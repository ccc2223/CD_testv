# ui/building_menu.py
"""
Building menu implementation for Castle Defense
"""
import pygame
from .base_menu import Menu
from .elements import Button
from features.buildings import Mine, Coresmith
from config import ITEM_COSTS

class BuildingMenu(Menu):
    """Menu for interacting with buildings"""
    def __init__(self, screen):
        """
        Initialize building menu
        
        Args:
            screen: Pygame surface to draw on
        """
        super().__init__(screen)
        self.building = None
        self.building_type = None
        self.resource_manager = None
    
    def set_building(self, building, building_type, resource_manager):
        """
        Set the building this menu controls
        
        Args:
            building: Building instance
            building_type: String type of building ("mine" or "coresmith")
            resource_manager: ResourceManager instance for resource costs
        """
        self.building = building
        self.building_type = building_type
        self.resource_manager = resource_manager
        self.title = f"{building_type.capitalize()} Menu"
        
        # Clear existing buttons
        self.buttons = []
        
        # Create buttons based on building type
        y_pos = self.rect.top + 50
        
        if building_type == "mine":
            # Mine upgrade button
            upgrade_button = Button(
                (self.rect.left + 20, y_pos),
                (self.rect.width - 40, 30),
                "Upgrade Mine",
                self.upgrade_mine
            )
            
            # Set button disabled state based on resources
            has_resources = self.resource_manager.has_resources(self.building.get_upgrade_cost())
            upgrade_button.set_disabled(not has_resources or self.building.upgrading)
            
            self.buttons.append(upgrade_button)
            
        elif building_type == "coresmith":
            # Item crafting buttons
            for i, item_name in enumerate(ITEM_COSTS.keys()):
                # Check if player has resources for this item
                has_resources = self.resource_manager.has_resources(ITEM_COSTS[item_name])
                is_crafting = self.building.crafting and self.building.current_item == item_name
                
                craft_button = Button(
                    (self.rect.left + 20, y_pos + i*40),
                    (self.rect.width - 40, 30),
                    f"Craft {item_name}",
                    lambda item=item_name: self.craft_item(item)
                )
                
                # Disable button if already crafting or not enough resources
                craft_button.set_disabled(not has_resources or self.building.crafting)
                
                self.buttons.append(craft_button)
    
    def upgrade_mine(self):
        """Upgrade the mine"""
        if isinstance(self.building, Mine) and self.resource_manager:
            if self.building.start_upgrade(self.resource_manager):
                # Disable button after successful upgrade start
                self.buttons[0].set_disabled(True)
    
    def craft_item(self, item_name):
        """
        Start crafting an item
        
        Args:
            item_name: Name of item to craft
        """
        if isinstance(self.building, Coresmith) and self.resource_manager:
            if self.building.start_crafting(item_name, self.resource_manager):
                # Disable all buttons after successful crafting start
                for button in self.buttons:
                    button.set_disabled(True)
    
    def update_button_states(self):
        """Update button disabled states based on current resources"""
        if not self.building or not self.resource_manager:
            return
            
        if self.building_type == "mine":
            # Update mine upgrade button
            has_resources = self.resource_manager.has_resources(self.building.get_upgrade_cost())
            self.buttons[0].set_disabled(not has_resources or self.building.upgrading)
            
        elif self.building_type == "coresmith":
            # Update coresmith crafting buttons
            for i, item_name in enumerate(ITEM_COSTS.keys()):
                has_resources = self.resource_manager.has_resources(ITEM_COSTS[item_name])
                self.buttons[i].set_disabled(not has_resources or self.building.crafting)
    
    def draw(self):
        """Draw building menu with building-specific info"""
        super().draw()
        
        if not self.active or not self.building:
            return
        
        # Update button states based on current resources
        self.update_button_states()
        
        # Draw building-specific information
        y_pos = self.rect.top + 120
        
        if self.building_type == "mine":
            # Draw mine info
            mine = self.building
            
            texts = [
                f"Level: {mine.level}",
                f"Resource: {mine.resource_type}",
                f"Production: {mine.production_rate:.1f}"
            ]
            
            for i, text in enumerate(texts):
                surface = self.small_font.render(text, True, (255, 255, 255))
                self.screen.blit(surface, (self.rect.left + 20, y_pos + i*20))
            
            # Draw upgrade progress if upgrading
            if mine.upgrading:
                progress_text = f"Upgrading: {int(mine.upgrade_timer)}/{int(mine.upgrade_time)}s"
                surface = self.small_font.render(progress_text, True, (100, 200, 255))
                self.screen.blit(surface, (self.rect.left + 20, y_pos + 80))
                
            # Draw upgrade cost
            else:
                upgrade_cost = mine.get_upgrade_cost()
                cost_text = "Upgrade Cost: " + ", ".join(f"{amt} {res}" for res, amt in upgrade_cost.items())
                
                # Color based on whether player has enough resources
                has_resources = self.resource_manager.has_resources(upgrade_cost)
                cost_color = (100, 255, 100) if has_resources else (255, 100, 100)
                
                surface = self.small_font.render(cost_text, True, cost_color)
                self.screen.blit(surface, (self.rect.left + 20, y_pos + 80))
        
        elif self.building_type == "coresmith":
            # Draw coresmith info
            coresmith = self.building
            
            # Draw crafting progress if crafting
            if coresmith.crafting:
                text = f"Crafting: {coresmith.current_item}"
                surface = self.small_font.render(text, True, (255, 255, 255))
                self.screen.blit(surface, (self.rect.left + 20, y_pos))
                
                progress_text = f"Time: {int(coresmith.crafting_timer)}/{int(coresmith.crafting_time)}s"
                surface = self.small_font.render(progress_text, True, (100, 200, 255))
                self.screen.blit(surface, (self.rect.left + 20, y_pos + 20))
            
            # Draw item costs
            y_pos += 60
            surface = self.small_font.render("Item Costs:", True, (255, 255, 255))
            self.screen.blit(surface, (self.rect.left + 20, y_pos))
            
            for i, (item_name, costs) in enumerate(ITEM_COSTS.items()):
                # Check if player has enough resources
                has_resources = self.resource_manager.has_resources(costs)
                cost_color = (200, 200, 200) if has_resources else (255, 100, 100)
                
                cost_text = f"{item_name}: " + ", ".join(f"{amt} {res}" for res, amt in costs.items())
                surface = self.small_font.render(cost_text, True, cost_color)
                self.screen.blit(surface, (self.rect.left + 20, y_pos + 20 + i*20))
