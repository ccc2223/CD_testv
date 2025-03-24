# tests/test_monsters.py
"""
Tests for modularized monster system
"""
import pygame
import unittest
from monsters import Monster, RegularMonster, BossMonster, WaveManager
from features.castle import Castle

class MonsterSystemTests(unittest.TestCase):
    """Test cases for monster system"""
    
    def setUp(self):
        """Set up test environment"""
        # Initialize pygame
        pygame.init()
        
        # Create dummy screen
        self.screen = pygame.Surface((800, 600))
        
        # Create castle instance for targeting
        self.castle = Castle()
        
        # Test positions
        self.start_pos = (100, 100)
        self.target_pos = (400, 400)
        
        # Test stats
        self.test_stats = {
            "health": 100,
            "speed": 50,
            "damage": 10
        }
    
    def test_base_monster_creation(self):
        """Test creating a base monster"""
        monster = Monster(self.start_pos, self.target_pos, "Test", self.test_stats)
        
        self.assertEqual(monster.health, 100)
        self.assertEqual(monster.damage, 10)
        self.assertFalse(monster.is_dead)
        self.assertFalse(monster.reached_castle)
    
    def test_regular_monster_creation(self):
        """Test creating a regular monster"""
        # RegularMonster gets stats from config, so we'll use a known type
        monster = RegularMonster(self.start_pos, self.target_pos, "Grunt")
        
        self.assertGreater(monster.health, 0)
        self.assertGreater(monster.damage, 0)
        self.assertEqual(monster.monster_type, "Grunt")
    
    def test_boss_monster_creation(self):
        """Test creating a boss monster"""
        # BossMonster gets stats from config, so we'll use a known type
        monster = BossMonster(self.start_pos, self.target_pos, "Force")
        
        self.assertGreater(monster.health, 0)
        self.assertGreater(monster.damage, 0)
        self.assertEqual(monster.monster_type, "Force")
        self.assertEqual(monster.core_drop, "Force Core")
    
    def test_wave_manager_creation(self):
        """Test creating a wave manager"""
        wave_manager = WaveManager()
        
        self.assertEqual(wave_manager.current_wave, 0)
        self.assertEqual(len(wave_manager.active_monsters), 0)
        self.assertFalse(wave_manager.wave_active)
        self.assertTrue(wave_manager.wave_completed)
    
    def test_monster_take_damage(self):
        """Test monster taking damage"""
        monster = Monster(self.start_pos, self.target_pos, "Test", self.test_stats)
        
        # Take damage but stay alive
        still_alive = monster.take_damage(50)
        self.assertTrue(still_alive)
        self.assertEqual(monster.health, 50)
        
        # Take fatal damage
        still_alive = monster.take_damage(50)
        self.assertFalse(still_alive)
        self.assertEqual(monster.health, 0)
        self.assertTrue(monster.is_dead)
    
    def test_boss_loot_drop(self):
        """Test boss loot drops"""
        boss = BossMonster(self.start_pos, self.target_pos, "Force")
        
        loot = boss.drop_loot()
        self.assertIn("Monster Coins", loot)
        self.assertIn("Force Core", loot)
        self.assertGreater(loot["Monster Coins"], 0)
        self.assertEqual(loot["Force Core"], 1)

if __name__ == "__main__":
    unittest.main()
