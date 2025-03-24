# ui/tower_menu.py
"""
Tower menu implementation for Castle Defense
"""
import pygame
from .base_menu import Menu
from .elements import Button
from features.towers import ArcherTower, SniperTower, SplashTower, FrozenTower
from config import (
    TOWER_TYPES, 
    TOWER_MONSTER_COIN_COSTS, 
    TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
    ITEM_COSTS, 
    ITEM_EFFECTS
)

class TowerMenu(Menu):
    """Menu for interacting with towers"""
    def __init__(self, screen):
        """
        Initialize tower menu
        
        Args:
            screen: Pygame surface to draw on
        """
        super().__init__(screen)
        self.tower = None
        self.resource_manager = None
        # Increase size to accommodate item slots and Monster Coin costs
        self.size = (280, 450)
        self.rect = pygame.Rect(self.position, self.size)
    
    def set_tower(self, tower, resource_manager):
        """
        Set the tower this menu controls
        
        Args:
            tower: Tower instance
            resource_manager: ResourceManager instance for resource costs
        """
        self.tower = tower
        self.resource_manager = resource_manager
        self.title = f"{tower.tower_type} Tower"
        
        # Clear existing buttons
        self.buttons = []
        
        # Create upgrade buttons
        y_pos = self.rect.top + 50
        button_width = (self.rect.width - 40)
        
        # Get damage upgrade costs
        damage_cost = tower.calculate_damage_upgrade_cost()
        damage_mc_cost = tower.calculate_damage_upgrade_monster_coin_cost()
        has_damage_resources = (self.resource_manager.has_resources(damage_cost) and 
                               self.resource_manager.get_resource("Monster Coins") >= damage_mc_cost)
        
        # Damage upgrade button
        damage_button = Button(
            (self.rect.left + 20, y_pos),
            (button_width, 30),
            "Upgrade Damage",
            self.upgrade_damage
        )
        damage_button.set_disabled(not has_damage_resources)
        self.buttons.append(damage_button)
        
        # Get attack speed upgrade costs
        speed_cost = tower.calculate_attack_speed_upgrade_cost()
        speed_mc_cost = tower.calculate_attack_speed_upgrade_monster_coin_cost()
        has_speed_resources = (self.resource_manager.has_resources(speed_cost) and
                              self.resource_manager.get_resource("Monster Coins") >= speed_mc_cost)
        
        # Attack speed upgrade button
        speed_button = Button(
            (self.rect.left + 20, y_pos + 40),
            (button_width, 30),
            "Upgrade Speed",
            self.upgrade_attack_speed
        )
        speed_button.set_disabled(not has_speed_resources)
        self.buttons.append(speed_button)
        
        # Get range upgrade costs
        range_cost = tower.calculate_range_upgrade_cost()
        range_mc_cost = tower.calculate_range_upgrade_monster_coin_cost()
        has_range_resources = (self.resource_manager.has_resources(range_cost) and
                              self.resource_manager.get_resource("Monster Coins") >= range_mc_cost)
        
        # Range upgrade button
        range_button = Button(
            (self.rect.left + 20, y_pos + 80),
            (button_width, 30),
            "Upgrade Range",
            self.upgrade_range
        )
        range_button.set_disabled(not has_range_resources)
        self.buttons.append(range_button)
        
        # Tower-specific upgrade buttons
        if isinstance(self.tower, SplashTower):
            # Get AoE upgrade costs
            aoe_cost = tower.calculate_aoe_radius_upgrade_cost()
            aoe_mc_cost = tower.calculate_aoe_radius_upgrade_monster_coin_cost()
            has_aoe_resources = (self.resource_manager.has_resources(aoe_cost) and
                               self.resource_manager.get_resource("Monster Coins") >= aoe_mc_cost)
            
            aoe_button = Button(
                (self.rect.left + 20, y_pos + 120),
                (button_width, 30),
                "Upgrade AoE",
                self.upgrade_aoe
            )
            aoe_button.set_disabled(not has_aoe_resources)
            self.buttons.append(aoe_button)
        
        elif isinstance(self.tower, FrozenTower):
            # Get slow effect upgrade costs
            slow_cost = tower.calculate_slow_effect_upgrade_cost()
            slow_mc_cost = tower.calculate_slow_effect_upgrade_monster_coin_cost()
            has_slow_resources = (self.resource_manager.has_resources(slow_cost) and
                                self.resource_manager.get_resource("Monster Coins") >= slow_mc_cost)
            
            slow_button = Button(
                (self.rect.left + 20, y_pos + 120),
                (button_width, 30),
                "Upgrade Slow Effect",
                self.upgrade_slow
            )
            slow_button.set_disabled(not has_slow_resources)
            self.buttons.append(slow_button)
            
            # Get slow duration upgrade costs
            duration_cost = tower.calculate_slow_duration_upgrade_cost()
            duration_mc_cost = tower.calculate_slow_duration_upgrade_monster_coin_cost()
            has_duration_resources = (self.resource_manager.has_resources(duration_cost) and
                                    self.resource_manager.get_resource("Monster Coins") >= duration_mc_cost)
            
            duration_button = Button(
                (self.rect.left + 20, y_pos + 160),
                (button_width, 30),
                "Upgrade Slow Duration",
                self.upgrade_slow_duration
            )
            duration_button.set_disabled(not has_duration_resources)
            self.buttons.append(duration_button)
            
        # Add item slot buttons
        # Calculate position for item slots section (below upgrades)
        items_y_pos = y_pos + 170
        if isinstance(self.tower, FrozenTower):
            # Adjust for extra button in FrozenTower
            items_y_pos += 40
        
        # Add heading for item slots
        item_header_y = items_y_pos
        
        # Item slot 1
        slot1_y = items_y_pos + 30
        # Get current item in slot 0
        current_item1 = tower.get_item_in_slot(0)
        
        if current_item1:
            # Create button to remove item
            remove_item1_button = Button(
                (self.rect.left + 20, slot1_y),
                (button_width, 30),
                f"Remove {current_item1}",
                lambda: self.remove_item_from_slot(0)
            )
            self.buttons.append(remove_item1_button)
        else:
            # Create buttons for available items
            for i, item_name in enumerate(["Unstoppable Force", "Serene Spirit"]):
                # Check if we have the item in inventory
                has_item = resource_manager.get_resource(item_name) > 0
                
                add_item_button = Button(
                    (self.rect.left + 20, slot1_y + i*35),
                    (button_width, 30),
                    f"Add {item_name} to Slot 1",
                    lambda item=item_name: self.add_item_to_slot(item, 0)
                )
                add_item_button.set_disabled(not has_item)
                self.buttons.append(add_item_button)
                
        # Item slot 2
        slot2_y = slot1_y + (0 if current_item1 else 70) + 40
        # Get current item in slot 1
        current_item2 = tower.get_item_in_slot(1)
        
        if current_item2:
            # Create button to remove item
            remove_item2_button = Button(
                (self.rect.left + 20, slot2_y),
                (button_width, 30),
                f"Remove {current_item2}",
                lambda: self.remove_item_from_slot(1)
            )
            self.buttons.append(remove_item2_button)
        else:
            # Create buttons for available items
            for i, item_name in enumerate(["Unstoppable Force", "Serene Spirit"]):
                # Check if we have the item in inventory
                has_item = resource_manager.get_resource(item_name) > 0
                
                add_item_button = Button(
                    (self.rect.left + 20, slot2_y + i*35),
                    (button_width, 30),
                    f"Add {item_name} to Slot 2",
                    lambda item=item_name: self.add_item_to_slot(item, 1)
                )
                add_item_button.set_disabled(not has_item)
                self.buttons.append(add_item_button)
    
    def add_item_to_slot(self, item, slot_index):
        """
        Add item to tower slot
        
        Args:
            item: Item name to add
            slot_index: Slot index (0 or 1)
        """
        if self.tower and self.resource_manager:
            if self.tower.add_item(item, slot_index, self.resource_manager):
                # Refresh menu to show updated slots
                self.set_tower(self.tower, self.resource_manager)
    
    def remove_item_from_slot(self, slot_index):
        """
        Remove item from tower slot
        
        Args:
            slot_index: Slot index (0 or 1)
        """
        if self.tower and self.resource_manager:
            removed_item = self.tower.remove_item(slot_index, self.resource_manager)
            if removed_item:
                # Refresh menu to show updated slots
                self.set_tower(self.tower, self.resource_manager)
    
    def upgrade_damage(self):
        """Upgrade tower damage"""
        if self.tower and self.resource_manager:
            if self.tower.upgrade_damage(self.resource_manager):
                # Update button states after successful upgrade
                self.update_button_states()
    
    def upgrade_attack_speed(self):
        """Upgrade tower attack speed"""
        if self.tower and self.resource_manager:
            if self.tower.upgrade_attack_speed(self.resource_manager):
                # Update button states after successful upgrade
                self.update_button_states()
    
    def upgrade_range(self):
        """Upgrade tower range"""
        if self.tower and self.resource_manager:
            if self.tower.upgrade_range(self.resource_manager):
                # Update button states after successful upgrade
                self.update_button_states()
    
    def upgrade_aoe(self):
        """Upgrade splash tower AoE radius"""
        if isinstance(self.tower, SplashTower) and self.resource_manager:
            if self.tower.upgrade_aoe_radius(self.resource_manager):
                # Update button states after successful upgrade
                self.update_button_states()
    
    def upgrade_slow(self):
        """Upgrade frozen tower slow effect"""
        if isinstance(self.tower, FrozenTower) and self.resource_manager:
            if self.tower.upgrade_slow_effect(self.resource_manager):
                # Update button states after successful upgrade
                self.update_button_states()
    
    def upgrade_slow_duration(self):
        """Upgrade frozen tower slow duration"""
        if isinstance(self.tower, FrozenTower) and self.resource_manager:
            if self.tower.upgrade_slow_duration(self.resource_manager):
                # Update button states after successful upgrade
                self.update_button_states()
    
    def update_button_states(self):
        """Update button disabled states based on current resources"""
        if not self.tower or not self.resource_manager:
            return
        
        # Update base upgrade buttons
        
        # Damage upgrade button (index 0)
        damage_cost = self.tower.calculate_damage_upgrade_cost()
        damage_mc_cost = self.tower.calculate_damage_upgrade_monster_coin_cost()
        has_damage_resources = (self.resource_manager.has_resources(damage_cost) and 
                               self.resource_manager.get_resource("Monster Coins") >= damage_mc_cost)
        self.buttons[0].set_disabled(not has_damage_resources)
        
        # Attack speed upgrade button (index 1)
        speed_cost = self.tower.calculate_attack_speed_upgrade_cost()
        speed_mc_cost = self.tower.calculate_attack_speed_upgrade_monster_coin_cost()
        has_speed_resources = (self.resource_manager.has_resources(speed_cost) and
                              self.resource_manager.get_resource("Monster Coins") >= speed_mc_cost)
        self.buttons[1].set_disabled(not has_speed_resources)
        
        # Range upgrade button (index 2)
        range_cost = self.tower.calculate_range_upgrade_cost()
        range_mc_cost = self.tower.calculate_range_upgrade_monster_coin_cost()
        has_range_resources = (self.resource_manager.has_resources(range_cost) and
                              self.resource_manager.get_resource("Monster Coins") >= range_mc_cost)
        self.buttons[2].set_disabled(not has_range_resources)
        
        # Tower-specific upgrade buttons
        if isinstance(self.tower, SplashTower):
            # AoE upgrade button (index 3)
            aoe_cost = self.tower.calculate_aoe_radius_upgrade_cost()
            aoe_mc_cost = self.tower.calculate_aoe_radius_upgrade_monster_coin_cost()
            has_aoe_resources = (self.resource_manager.has_resources(aoe_cost) and
                               self.resource_manager.get_resource("Monster Coins") >= aoe_mc_cost)
            self.buttons[3].set_disabled(not has_aoe_resources)
            
        elif isinstance(self.tower, FrozenTower):
            # Slow effect upgrade button (index 3)
            slow_cost = self.tower.calculate_slow_effect_upgrade_cost()
            slow_mc_cost = self.tower.calculate_slow_effect_upgrade_monster_coin_cost()
            has_slow_resources = (self.resource_manager.has_resources(slow_cost) and
                                self.resource_manager.get_resource("Monster Coins") >= slow_mc_cost)
            self.buttons[3].set_disabled(not has_slow_resources)
            
            # Slow duration upgrade button (index 4)
            duration_cost = self.tower.calculate_slow_duration_upgrade_cost()
            duration_mc_cost = self.tower.calculate_slow_duration_upgrade_monster_coin_cost()
            has_duration_resources = (self.resource_manager.has_resources(duration_cost) and
                                    self.resource_manager.get_resource("Monster Coins") >= duration_mc_cost)
            self.buttons[4].set_disabled(not has_duration_resources)
        
        # Update item buttons (they're after the upgrade buttons)
        item_button_start = 3
        if isinstance(self.tower, SplashTower):
            item_button_start = 4
        elif isinstance(self.tower, FrozenTower):
            item_button_start = 5
            
        for i in range(item_button_start, len(self.buttons)):
            # If button contains "Add" in text, check if we have the item
            button_text = self.buttons[i].text
            if "Add " in button_text:
                item_name = button_text.split("Add ")[1].split(" to")[0]
                has_item = self.resource_manager.get_resource(item_name) > 0
                self.buttons[i].set_disabled(not has_item)
    
    def draw(self):
        """Draw tower menu with tower-specific info"""
        super().draw()
        
        if not self.active or not self.tower:
            return
        
        # Update button states based on current resources
        self.update_button_states()
        
        # Draw tower stats
        tower = self.tower
        y_pos = self.rect.top + 220
        
        # Draw upgrade information header
        upgrade_header = self.font.render("Upgrade Costs:", True, (255, 200, 100))
        upgrade_header_rect = upgrade_header.get_rect(midleft=(self.rect.left + 20, y_pos - 20))
        self.screen.blit(upgrade_header, upgrade_header_rect)
        
        # Draw upgrade cost explanation
        cost_info = self.small_font.render("(Requires both resources and Monster Coins)", True, (200, 200, 200))
        cost_info_rect = cost_info.get_rect(midleft=(self.rect.left + 30, y_pos))
        self.screen.blit(cost_info, cost_info_rect)
        y_pos += 25
        
        # Draw damage upgrade costs
        damage_cost = tower.calculate_damage_upgrade_cost()
        damage_mc_cost = tower.calculate_damage_upgrade_monster_coin_cost()
        
        # Check if player has enough resources and Monster Coins
        has_damage_resources = self.resource_manager.has_resources(damage_cost)
        has_damage_mc = self.resource_manager.get_resource("Monster Coins") >= damage_mc_cost
        
        # Resource costs
        resource_color = (100, 255, 100) if has_damage_resources else (255, 100, 100)
        damage_cost_text = "Damage: " + ", ".join(f"{amt} {res}" for res, amt in damage_cost.items())
        damage_cost_surface = self.small_font.render(damage_cost_text, True, resource_color)
        self.screen.blit(damage_cost_surface, (self.rect.left + 20, y_pos))
        
        # Monster Coin cost
        mc_color = (100, 255, 100) if has_damage_mc else (255, 100, 100)
        mc_text = f"+ {damage_mc_cost} Monster Coins"
        mc_surface = self.small_font.render(mc_text, True, mc_color)
        self.screen.blit(mc_surface, (self.rect.left + 35, y_pos + 15))
        y_pos += 35
        
        # Draw speed upgrade costs
        speed_cost = tower.calculate_attack_speed_upgrade_cost()
        speed_mc_cost = tower.calculate_attack_speed_upgrade_monster_coin_cost()
        
        # Check if player has enough resources and Monster Coins
        has_speed_resources = self.resource_manager.has_resources(speed_cost)
        has_speed_mc = self.resource_manager.get_resource("Monster Coins") >= speed_mc_cost
        
        # Resource costs
        resource_color = (100, 255, 100) if has_speed_resources else (255, 100, 100)
        speed_cost_text = "Speed: " + ", ".join(f"{amt} {res}" for res, amt in speed_cost.items())
        speed_cost_surface = self.small_font.render(speed_cost_text, True, resource_color)
        self.screen.blit(speed_cost_surface, (self.rect.left + 20, y_pos))
        
        # Monster Coin cost
        mc_color = (100, 255, 100) if has_speed_mc else (255, 100, 100)
        mc_text = f"+ {speed_mc_cost} Monster Coins"
        mc_surface = self.small_font.render(mc_text, True, mc_color)
        self.screen.blit(mc_surface, (self.rect.left + 35, y_pos + 15))
        y_pos += 35
        
        # Draw range upgrade costs
        range_cost = tower.calculate_range_upgrade_cost()
        range_mc_cost = tower.calculate_range_upgrade_monster_coin_cost()
        
        # Check if player has enough resources and Monster Coins
        has_range_resources = self.resource_manager.has_resources(range_cost)
        has_range_mc = self.resource_manager.get_resource("Monster Coins") >= range_mc_cost
        
        # Resource costs
        resource_color = (100, 255, 100) if has_range_resources else (255, 100, 100)
        range_cost_text = "Range: " + ", ".join(f"{amt} {res}" for res, amt in range_cost.items())
        range_cost_surface = self.small_font.render(range_cost_text, True, resource_color)
        self.screen.blit(range_cost_surface, (self.rect.left + 20, y_pos))
        
        # Monster Coin cost
        mc_color = (100, 255, 100) if has_range_mc else (255, 100, 100)
        mc_text = f"+ {range_mc_cost} Monster Coins"
        mc_surface = self.small_font.render(mc_text, True, mc_color)
        self.screen.blit(mc_surface, (self.rect.left + 35, y_pos + 15))
        y_pos += 35
        
        # Draw tower-specific upgrade costs
        if isinstance(tower, SplashTower):
            aoe_cost = tower.calculate_aoe_radius_upgrade_cost()
            aoe_mc_cost = tower.calculate_aoe_radius_upgrade_monster_coin_cost()
            
            # Check if player has enough resources and Monster Coins
            has_aoe_resources = self.resource_manager.has_resources(aoe_cost)
            has_aoe_mc = self.resource_manager.get_resource("Monster Coins") >= aoe_mc_cost
            
            # Resource costs
            resource_color = (100, 255, 100) if has_aoe_resources else (255, 100, 100)
            aoe_cost_text = "AoE: " + ", ".join(f"{amt} {res}" for res, amt in aoe_cost.items())
            aoe_cost_surface = self.small_font.render(aoe_cost_text, True, resource_color)
            self.screen.blit(aoe_cost_surface, (self.rect.left + 20, y_pos))
            
            # Monster Coin cost
            mc_color = (100, 255, 100) if has_aoe_mc else (255, 100, 100)
            mc_text = f"+ {aoe_mc_cost} Monster Coins"
            mc_surface = self.small_font.render(mc_text, True, mc_color)
            self.screen.blit(mc_surface, (self.rect.left + 35, y_pos + 15))
            y_pos += 35
            
        elif isinstance(tower, FrozenTower):
            slow_cost = tower.calculate_slow_effect_upgrade_cost()
            slow_mc_cost = tower.calculate_slow_effect_upgrade_monster_coin_cost()
            
            # Check if player has enough resources and Monster Coins
            has_slow_resources = self.resource_manager.has_resources(slow_cost)
            has_slow_mc = self.resource_manager.get_resource("Monster Coins") >= slow_mc_cost
            
            # Resource costs
            resource_color = (100, 255, 100) if has_slow_resources else (255, 100, 100)
            slow_cost_text = "Slow: " + ", ".join(f"{amt} {res}" for res, amt in slow_cost.items())
            slow_cost_surface = self.small_font.render(slow_cost_text, True, resource_color)
            self.screen.blit(slow_cost_surface, (self.rect.left + 20, y_pos))
            
            # Monster Coin cost
            mc_color = (100, 255, 100) if has_slow_mc else (255, 100, 100)
            mc_text = f"+ {slow_mc_cost} Monster Coins"
            mc_surface = self.small_font.render(mc_text, True, mc_color)
            self.screen.blit(mc_surface, (self.rect.left + 35, y_pos + 15))
            y_pos += 35
            
            duration_cost = tower.calculate_slow_duration_upgrade_cost()
            duration_mc_cost = tower.calculate_slow_duration_upgrade_monster_coin_cost()
            
            # Check if player has enough resources and Monster Coins
            has_duration_resources = self.resource_manager.has_resources(duration_cost)
            has_duration_mc = self.resource_manager.get_resource("Monster Coins") >= duration_mc_cost
            
            # Resource costs
            resource_color = (100, 255, 100) if has_duration_resources else (255, 100, 100)
            duration_cost_text = "Duration: " + ", ".join(f"{amt} {res}" for res, amt in duration_cost.items())
            duration_cost_surface = self.small_font.render(duration_cost_text, True, resource_color)
            self.screen.blit(duration_cost_surface, (self.rect.left + 20, y_pos))
            
            # Monster Coin cost
            mc_color = (100, 255, 100) if has_duration_mc else (255, 100, 100)
            mc_text = f"+ {duration_mc_cost} Monster Coins"
            mc_surface = self.small_font.render(mc_text, True, mc_color)
            self.screen.blit(mc_surface, (self.rect.left + 35, y_pos + 15))
            y_pos += 35
        
        # Adjust y_pos for stats based on tower type
        if isinstance(tower, SplashTower):
            y_pos += 5
        elif isinstance(tower, FrozenTower):
            y_pos += 5
        else:
            y_pos += 5
        
        # Draw stats header
        header_text = "Tower Stats:"
        header_surface = self.font.render(header_text, True, (255, 255, 255))
        header_rect = header_surface.get_rect(midleft=(self.rect.left + 20, y_pos))
        self.screen.blit(header_surface, header_rect)
        
        y_pos += 25
        
        # Base stats with item effect indicators
        base_damage = tower.base_damage
        base_attack_speed = tower.base_attack_speed
        base_range = tower.base_range
        
        texts = [
            f"Overall Level: {tower.level}",
            f"Damage (Lv {tower.damage_level}): {tower.damage:.1f}" + (f" (Base: {base_damage:.1f})" if tower.damage != base_damage else ""),
            f"Attack Speed (Lv {tower.attack_speed_level}): {tower.attack_speed:.2f}/s" + (f" (Base: {base_attack_speed:.2f})" if tower.attack_speed != base_attack_speed else ""),
            f"Range (Lv {tower.range_level}): {tower.range:.0f}" + (f" (Base: {base_range:.0f})" if tower.range != base_range else "")
        ]
        
        # Add tower-specific stats
        if isinstance(tower, SplashTower):
            base_aoe = tower.base_aoe_radius
            texts.append(f"AoE Radius (Lv {tower.aoe_radius_level}): {tower.aoe_radius:.0f}" + (f" (Base: {base_aoe:.0f})" if tower.aoe_radius != base_aoe else ""))
        elif isinstance(tower, FrozenTower):
            base_slow = tower.base_slow_effect
            base_duration = tower.base_slow_duration
            texts.append(f"Slow Effect (Lv {tower.slow_effect_level}): {tower.slow_effect*100:.0f}%" + (f" (Base: {base_slow*100:.0f}%)" if tower.slow_effect != base_slow else ""))
            texts.append(f"Slow Duration (Lv {tower.slow_duration_level}): {tower.slow_duration:.1f}s" + (f" (Base: {base_duration:.1f}s)" if tower.slow_duration != base_duration else ""))
        
        for i, text in enumerate(texts):
            surface = self.small_font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (self.rect.left + 20, y_pos + i*20))
            
        # Draw items section header
        items_y = y_pos + len(texts)*20 + 20
        header_text = "Item Slots:"
        header_surface = self.font.render(header_text, True, (255, 255, 255))
        header_rect = header_surface.get_rect(midleft=(self.rect.left + 20, items_y))
        self.screen.blit(header_surface, header_rect)
        
        items_y += 25
        
        # Draw current items
        for i in range(2):
            item = tower.get_item_in_slot(i)
            
            slot_text = f"Slot {i+1}: " + (item if item else "Empty")
            slot_color = (255, 255, 255) if item else (150, 150, 150)
            
            slot_surface = self.small_font.render(slot_text, True, slot_color)
            self.screen.blit(slot_surface, (self.rect.left + 20, items_y + i*45))
            
            # If item is equipped, draw its effect
            if item:
                effect_desc = ITEM_EFFECTS.get(item, {}).get("description", "")
                effect_surface = self.small_font.render(f"  - {effect_desc}", True, (200, 200, 255))
                self.screen.blit(effect_surface, (self.rect.left + 30, items_y + i*45 + 20))
