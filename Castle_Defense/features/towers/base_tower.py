# towers/base_tower.py
"""
Base Tower class for Castle Defense
"""
import pygame
import math
from config import (
    TOWER_TYPES,
    TOWER_UPGRADE_COST_MULTIPLIER,
    TOWER_MONSTER_COIN_COSTS,
    TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER,
    TOWER_DAMAGE_UPGRADE_MULTIPLIER,
    TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER,
    TOWER_RANGE_UPGRADE_MULTIPLIER,
    TOWER_AOE_UPGRADE_MULTIPLIER,
    ITEM_EFFECTS
)
from utils import distance, calculate_angle, scale_position, scale_size, scale_value

class Tower:
    """Base class for all towers"""
    def __init__(self, position, tower_type):
        """
        Initialize tower with position and type
        
        Args:
            position: Tuple of (x, y) coordinates
            tower_type: String indicating tower type
        """
        self.position = position
        self.tower_type = tower_type
        self.level = 1
        
        # Individual upgrade path levels
        self.damage_level = 1
        self.attack_speed_level = 1
        self.range_level = 1
        
        # Set stats from config - scale range based on screen size
        tower_config = TOWER_TYPES.get(tower_type, {})
        self.damage = tower_config.get("damage", 10)
        self.attack_speed = tower_config.get("attack_speed", 1.0)
        
        # Store both reference and scaled range
        self.ref_range = tower_config.get("range", 150)
        self.range = scale_value(self.ref_range)
        
        # Store base stats for item effect calculations
        self.base_damage = self.damage
        self.base_attack_speed = self.attack_speed
        self.base_range = self.range
        self.base_ref_range = self.ref_range
        
        # Attack tracking
        self.attack_timer = 0
        self.targets = []
        self.current_target = None  # Track current target for animations
        
        # Animation flags
        self.is_attacking = False
        self.attack_animation_time = 0
        
        # Item slots
        self.item_slots = [None, None]
        self.has_item_effects = False
        
        # Splash damage from Unstoppable Force (for single-target towers)
        self.splash_damage_enabled = False
        self.splash_damage_radius = 0
        
        # Item visual effects
        self.item_glow_color = None
        self.item_glow_intensity = 0
        
        # Visual properties
        self.ref_size = (40, 40)
        self.size = scale_size(self.ref_size)
        self.rect = pygame.Rect(
            position[0] - self.size[0] // 2,
            position[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )
        self.color = self.get_color_from_type(tower_type)
        
        # For selection and highlight
        self.selected = False
        
        # Tower-specific properties
        self.initialize_specific_properties()
    
    def get_color_from_type(self, tower_type):
        """
        Get color based on tower type
        
        Args:
            tower_type: String indicating tower type
            
        Returns:
            RGB color tuple
        """
        colors = {
            "Archer": (100, 150, 100),  # Green
            "Sniper": (150, 100, 100),  # Red
            "Splash": (150, 150, 100),  # Yellow
            "Frozen": (100, 150, 150)   # Cyan
        }
        return colors.get(tower_type, (100, 100, 100))
    
    def initialize_specific_properties(self):
        """Initialize tower-specific properties"""
        tower_config = TOWER_TYPES.get(self.tower_type, {})
        
        # Initialize AoE properties for Splash tower
        if self.tower_type == "Splash":
            self.ref_aoe_radius = tower_config.get("aoe_radius", 50)
            self.aoe_radius = scale_value(self.ref_aoe_radius)
            # Store base AoE for item effects
            self.base_ref_aoe_radius = self.ref_aoe_radius
            self.base_aoe_radius = self.aoe_radius
            # Add AoE upgrade level
            self.aoe_radius_level = 1
        
        # Initialize slow properties for Frozen tower
        elif self.tower_type == "Frozen":
            self.slow_effect = tower_config.get("slow_effect", 0.5)
            self.slow_duration = tower_config.get("slow_duration", 3.0)
            # Store base slow effect for item effects
            self.base_slow_effect = self.slow_effect
            self.base_slow_duration = self.slow_duration
            # Add slow upgrade levels
            self.slow_effect_level = 1
            self.slow_duration_level = 1
    
    def update(self, dt, monsters, animation_manager=None):
        """
        Update tower state and attack monsters
        
        Args:
            dt: Time delta in seconds
            monsters: List of monsters to target
            animation_manager: Optional AnimationManager for visual effects
        """
        # Update attack animation flag if needed
        if self.is_attacking:
            self.attack_animation_time -= dt
            if self.attack_animation_time <= 0:
                self.is_attacking = False
        
        # Update item glow effect
        if self.item_glow_color:
            # Pulsing glow effect
            self.item_glow_intensity = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.005)
        
        # Find targets
        self.find_targets(monsters)
        
        # Update attack timer
        self.attack_timer += dt
        if self.attack_timer >= 1.0 / self.attack_speed and self.targets:
            self.attack_timer = 0
            self.attack(animation_manager)
    
    def find_targets(self, monsters):
        """
        Find valid targets within range
        
        Args:
            monsters: List of monsters to check
        """
        self.targets = []
        
        for monster in monsters:
            # Skip dead monsters
            if monster.is_dead:
                continue
                
            # Skip flying monsters unless we're an Archer or Sniper tower
            if monster.flying and self.tower_type not in ["Archer", "Sniper"]:
                continue
            
            # Check if monster is in range
            if distance(self.position, monster.position) <= self.range:
                self.targets.append(monster)
        
        # Sort targets by distance (closest first)
        self.targets.sort(key=lambda m: distance(self.position, m.position))
    
    def attack(self, animation_manager=None):
        """
        Attack targets
        
        Args:
            animation_manager: Optional AnimationManager for visual effects
        """
        # Set attacking flag and animation time
        self.is_attacking = True
        self.attack_animation_time = 0.5  # Animation duration in seconds
        
        # Store current target for animation
        if self.targets:
            self.current_target = self.targets[0]
            
            # Create attack animation if animation manager is provided
            if animation_manager and self.current_target:
                animation_manager.create_tower_attack_animation(self, self.current_target)
    
    def calculate_damage_upgrade_cost(self):
        """
        Calculate upgrade cost for damage based on damage level
        
        Returns:
            Dictionary of resource costs
        """
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with damage level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.damage_level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def calculate_damage_upgrade_monster_coin_cost(self):
        """
        Calculate Monster Coin cost for damage upgrade based on damage level
        
        Returns:
            Integer Monster Coin cost
        """
        base_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 5)
        return int(base_cost * (TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER ** (self.damage_level - 1)))
    
    def calculate_attack_speed_upgrade_cost(self):
        """
        Calculate upgrade cost for attack speed based on attack speed level
        
        Returns:
            Dictionary of resource costs
        """
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with attack speed level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.attack_speed_level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def calculate_attack_speed_upgrade_monster_coin_cost(self):
        """
        Calculate Monster Coin cost for attack speed upgrade based on attack speed level
        
        Returns:
            Integer Monster Coin cost
        """
        base_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 5)
        return int(base_cost * (TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER ** (self.attack_speed_level - 1)))
    
    def calculate_range_upgrade_cost(self):
        """
        Calculate upgrade cost for range based on range level
        
        Returns:
            Dictionary of resource costs
        """
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with range level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.range_level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def calculate_range_upgrade_monster_coin_cost(self):
        """
        Calculate Monster Coin cost for range upgrade based on range level
        
        Returns:
            Integer Monster Coin cost
        """
        base_cost = TOWER_MONSTER_COIN_COSTS.get(self.tower_type, 5)
        return int(base_cost * (TOWER_MONSTER_COIN_UPGRADE_MULTIPLIER ** (self.range_level - 1)))
    
    def upgrade_damage(self, resource_manager):
        """
        Upgrade tower damage
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        cost = self.calculate_damage_upgrade_cost()
        monster_coin_cost = self.calculate_damage_upgrade_monster_coin_cost()
        
        # Check if we have enough resources and Monster Coins
        if not resource_manager.has_resources(cost) or resource_manager.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        # Spend resources and Monster Coins
        if resource_manager and resource_manager.spend_resources(cost):
            # Spend the Monster Coins separately
            resource_manager.spend_resource("Monster Coins", monster_coin_cost)
            
            self.base_damage *= TOWER_DAMAGE_UPGRADE_MULTIPLIER
            self.damage_level += 1
            self.level += 1  # Keep overall level for compatibility
            self.apply_item_effects()  # Re-apply item effects after upgrade
            return True
        return False
    
    def upgrade_attack_speed(self, resource_manager):
        """
        Upgrade tower attack speed
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        cost = self.calculate_attack_speed_upgrade_cost()
        monster_coin_cost = self.calculate_attack_speed_upgrade_monster_coin_cost()
        
        # Check if we have enough resources and Monster Coins
        if not resource_manager.has_resources(cost) or resource_manager.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        # Spend resources and Monster Coins
        if resource_manager and resource_manager.spend_resources(cost):
            # Spend the Monster Coins separately
            resource_manager.spend_resource("Monster Coins", monster_coin_cost)
            
            self.base_attack_speed *= TOWER_ATTACK_SPEED_UPGRADE_MULTIPLIER
            self.attack_speed_level += 1
            self.level += 1  # Keep overall level for compatibility
            self.apply_item_effects()  # Re-apply item effects after upgrade
            return True
        return False
    
    def upgrade_range(self, resource_manager):
        """
        Upgrade tower range
        
        Args:
            resource_manager: ResourceManager to spend resources
            
        Returns:
            True if upgrade successful, False if insufficient resources
        """
        cost = self.calculate_range_upgrade_cost()
        monster_coin_cost = self.calculate_range_upgrade_monster_coin_cost()
        
        # Check if we have enough resources and Monster Coins
        if not resource_manager.has_resources(cost) or resource_manager.get_resource("Monster Coins") < monster_coin_cost:
            return False
            
        # Spend resources and Monster Coins
        if resource_manager and resource_manager.spend_resources(cost):
            # Spend the Monster Coins separately
            resource_manager.spend_resource("Monster Coins", monster_coin_cost)
            
            # Upgrade both reference and scaled range
            self.base_ref_range *= TOWER_RANGE_UPGRADE_MULTIPLIER
            self.base_range = scale_value(self.base_ref_range)
            self.range_level += 1
            self.level += 1  # Keep overall level for compatibility
            self.apply_item_effects()  # Re-apply item effects after upgrade
            return True
        return False
    
    def calculate_upgrade_cost(self):
        """
        Calculate general upgrade cost (for compatibility)
        
        Returns:
            Dictionary of resource costs
        """
        # This is kept for backward compatibility
        base_cost = TOWER_TYPES.get(self.tower_type, {}).get("cost", {"Stone": 20})
        
        # Scale cost with tower level
        return {
            resource_type: int(amount * (TOWER_UPGRADE_COST_MULTIPLIER ** (self.level - 1)))
            for resource_type, amount in base_cost.items()
        }
    
    def add_item(self, item, slot_index, resource_manager=None):
        """
        Add item to tower
        
        Args:
            item: Item to add
            slot_index: Slot index to place item (0 or 1)
            resource_manager: Optional ResourceManager to handle resource changes
            
        Returns:
            True if item added, False if invalid slot
        """
        if 0 <= slot_index < len(self.item_slots):
            # Remove current item if present
            current_item = self.item_slots[slot_index]
            if current_item and resource_manager:
                # Return the old item to inventory
                resource_manager.add_resource(current_item, 1)
            
            # Add new item
            self.item_slots[slot_index] = item
            
            # Spend the item from inventory if resource_manager provided
            if resource_manager and item:
                resource_manager.spend_resource(item, 1)
            
            # Apply effects of all equipped items
            self.apply_item_effects()
            return True
        return False
    
    def remove_item(self, slot_index, resource_manager=None):
        """
        Remove item from tower
        
        Args:
            slot_index: Slot index to remove item from (0 or 1)
            resource_manager: Optional ResourceManager to handle resource changes
            
        Returns:
            Name of removed item or None
        """
        if 0 <= slot_index < len(self.item_slots) and self.item_slots[slot_index]:
            removed_item = self.item_slots[slot_index]
            self.item_slots[slot_index] = None
            
            # Reset stats and recalculate based on remaining items
            self.apply_item_effects()
            
            # Add the item back to inventory if resource_manager provided
            if resource_manager:
                resource_manager.add_resource(removed_item, 1)
                
            return removed_item
        
        return None
    
    def apply_item_effects(self):
        """Apply effects from equipped items"""
        # Reset stats to base values
        self.damage = self.base_damage
        self.attack_speed = self.base_attack_speed
        self.ref_range = self.base_ref_range
        self.range = self.base_range
        
        # Reset tower-specific properties
        if self.tower_type == "Splash":
            self.ref_aoe_radius = self.base_ref_aoe_radius
            self.aoe_radius = self.base_aoe_radius
        elif self.tower_type == "Frozen":
            self.slow_effect = self.base_slow_effect
            self.slow_duration = self.base_slow_duration
        
        # Reset splash damage (for single-target towers)
        self.splash_damage_enabled = False
        self.splash_damage_radius = 0
        
        # Reset item visual effects
        self.item_glow_color = None
        
        # No item effects to apply if both slots are empty
        if not any(self.item_slots):
            self.has_item_effects = False
            return
            
        self.has_item_effects = True
        
        # Apply effects from each equipped item
        for item in self.item_slots:
            if not item:
                continue
                
            # Get item effect information
            item_effect = ITEM_EFFECTS.get(item, {})
            
            # Apply Unstoppable Force effects
            if item == "Unstoppable Force":
                # Update visual effect
                self.item_glow_color = item_effect.get("glow_color", (255, 100, 50))
                
                # Apply AoE increase to AoE towers
                if self.tower_type in ["Splash", "Frozen"]:
                    aoe_multiplier = item_effect.get("aoe_radius_multiplier", 1.3)
                    
                    if self.tower_type == "Splash":
                        self.ref_aoe_radius *= aoe_multiplier
                        self.aoe_radius = scale_value(self.ref_aoe_radius)
                    elif self.tower_type == "Frozen":
                        # For Frozen Tower, increase slow effect area (which is the range)
                        self.ref_range *= aoe_multiplier
                        self.range = scale_value(self.ref_range)
                
                # Apply splash damage for single-target towers
                elif self.tower_type in ["Archer", "Sniper"]:
                    self.splash_damage_enabled = True
                    # Scale splash radius with tower range
                    base_splash = item_effect.get("splash_damage_radius", 30)
                    self.splash_damage_radius = scale_value(base_splash)
                    
            # Apply Serene Spirit effects (not implemented yet)
            elif item == "Serene Spirit":
                # Update visual effect
                self.item_glow_color = item_effect.get("glow_color", (100, 200, 100))
                # Implementation for healing effect will be added later
    
    def get_item_in_slot(self, slot_index):
        """
        Get item in specified slot
        
        Args:
            slot_index: Slot index to check (0 or 1)
            
        Returns:
            Item name or None if slot is empty or invalid
        """
        if 0 <= slot_index < len(self.item_slots):
            return self.item_slots[slot_index]
        return None
    
    def draw(self, screen):
        """
        Draw tower to screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw tower base
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw item glow effect if tower has items
        if self.item_glow_color and self.item_glow_intensity > 0:
            # Create the glow as a transparent surface
            glow_size = int(self.size[0] * (1.2 + 0.1 * self.item_glow_intensity))
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            
            # Calculate glow color with alpha based on intensity
            glow_alpha = int(100 * self.item_glow_intensity)
            glow_color = (*self.item_glow_color, glow_alpha)
            
            # Draw the glow
            pygame.draw.rect(glow_surface, glow_color, 
                           (0, 0, glow_size, glow_size), 
                           int(self.size[0] * 0.2))
            
            # Position the glow centered on the tower
            glow_pos = (
                self.position[0] - glow_size // 2,
                self.position[1] - glow_size // 2
            )
            
            # Draw the glow
            screen.blit(glow_surface, glow_pos)
        
        # Draw tower
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw tower type indicator
        font_size = scale_value(16)
        font = pygame.font.Font(None, font_size)
        text = font.render(self.tower_type, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - scale_value(10)))
        screen.blit(text, text_rect)
        
        # Draw tower level
        font_size = scale_value(20)
        font = pygame.font.Font(None, font_size)
        text = font.render(f"Lv {self.level}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text, text_rect)
        
        # Draw item indicators if tower has items
        if any(self.item_slots):
            small_font = pygame.font.Font(None, scale_value(14))
            for i, item in enumerate(self.item_slots):
                if item:
                    # Calculate position for item indicator (top-left and top-right corners)
                    x_offset = -self.size[0]//2 + scale_value(8) if i == 0 else self.size[0]//2 - scale_value(8)
                    item_pos = (self.rect.centerx + x_offset, self.rect.top - scale_value(25))
                    
                    # Get first letter of item for indicator
                    item_letter = item[0]
                    
                    # Draw background circle
                    if item == "Unstoppable Force":
                        bg_color = (255, 100, 50)  # Orange for Unstoppable Force
                    elif item == "Serene Spirit":
                        bg_color = (100, 200, 100)  # Green for Serene Spirit
                    else:
                        bg_color = (150, 150, 150)  # Gray for other items
                        
                    pygame.draw.circle(screen, bg_color, item_pos, scale_value(8))
                    
                    # Draw item letter
                    text = small_font.render(item_letter, True, (255, 255, 255))
                    text_rect = text.get_rect(center=item_pos)
                    screen.blit(text, text_rect)
        
        # Draw attack animation (flash or highlight when attacking)
        if self.is_attacking:
            # Calculate highlight intensity based on animation time
            intensity = self.attack_animation_time * 2  # 0.0 to 1.0
            highlight_color = (
                min(255, self.color[0] + 50 * intensity),
                min(255, self.color[1] + 50 * intensity),
                min(255, self.color[2] + 50 * intensity)
            )
            highlight_rect = self.rect.inflate(scale_value(4), scale_value(4))
            pygame.draw.rect(screen, highlight_color, highlight_rect, scale_value(2))
        
        # Draw range indicator (only when selected)
        if self.selected:
            # Draw main range circle
            pygame.draw.circle(screen, (255, 255, 255), 
                              (int(self.position[0]), int(self.position[1])), 
                              int(self.range), scale_value(1))
            
            # Draw special range indicators based on tower type and items
            if self.tower_type == "Splash":
                # Draw AoE radius indicator for Splash Tower
                pygame.draw.circle(screen, (255, 200, 0), 
                                  (int(self.position[0]), int(self.position[1])), 
                                  int(self.aoe_radius), scale_value(1))
                
            elif self.tower_type in ["Archer", "Sniper"] and self.splash_damage_enabled:
                # Draw splash damage radius for single-target towers with Unstoppable Force
                pygame.draw.circle(screen, (255, 150, 50), 
                                  (int(self.position[0]), int(self.position[1])), 
                                  int(self.splash_damage_radius), scale_value(1))
