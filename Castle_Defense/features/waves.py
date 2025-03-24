# features/waves.py
"""
Wave and monster spawning system for Castle Defense - Updated to use modularized monster system
"""
# Re-export all monster classes and wave manager from the monsters package
# This ensures backward compatibility with existing code
from features.monsters.base_monster import Monster
from features.monsters.regular_monster import RegularMonster
from features.monsters.boss_monster import BossMonster
from features.monsters.wave_manager import WaveManager
from features.monsters.factory import MonsterFactory

__all__ = ['Monster', 'RegularMonster', 'BossMonster', 'WaveManager', 'MonsterFactory']
