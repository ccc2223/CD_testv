# features/monsters/__init__.py
"""
Monster system package for Castle Defense.
Contains monster implementations and wave management.
"""
from .base_monster import Monster
from .regular_monster import RegularMonster
from .boss_monster import BossMonster
from .wave_manager import WaveManager
from .factory import MonsterFactory

__all__ = ['Monster', 'RegularMonster', 'BossMonster', 'WaveManager', 'MonsterFactory']
