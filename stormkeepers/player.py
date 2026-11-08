"""Persistent character data and level progression."""
from dataclasses import dataclass, field, asdict
from skill import SKILLS
from ui import say

@dataclass
class Player:
    name: str
    hp: int = 100
    level: int = 1
    xp: int = 0
    gold: int = 40
    inventory: dict = field(default_factory=lambda: {'rainwater': 3})
    skills: list = field(default_factory=lambda: ['lightning'])
    map_name: str = 'valley'
    x: int = 1
    y: int = 1
    quest: int = 0
    side: dict = field(default_factory=lambda: {'shards': False, 'patrol': False})
    kills: int = 0
    shield: int = 0
    cleared_monsters: list = field(default_factory=list)

    @property
    def max_hp(self):
        return 100 + (self.level - 1) * 20

    @property
    def attack(self):
        return 16 + (self.level - 1) * 4

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 35:
            self.xp -= self.level * 35
            self.level += 1
            self.hp = self.max_hp
            say(f'Level {self.level}! Health restored.', 'good')

    def to_data(self):
        data = asdict(self)
        data['shield'] = 0  # Combat effects never persist outside a battle.
        return data

    @classmethod
    def from_data(cls, data):
        return cls(**data)

    def show(self):
        say(f'{self.name} | Level {self.level} | XP {self.xp}/{self.level * 35}')
        say(f'HP {self.hp}/{self.max_hp} | Attack {self.attack} | Gold {self.gold}', 'gold')
        say('Skills: ' + ', '.join(SKILLS[s].name for s in self.skills))
        say(f'Location: {self.map_name} ({self.x}, {self.y}) | Victories: {self.kills}')
