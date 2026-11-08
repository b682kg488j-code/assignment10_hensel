"""Five enemies inherit shared state and override stats or behavior."""
class Monster:
    name, health, attack, xp, gold = 'Weather spirit', 30, 6, 12, 10
    def __init__(self):
        self.hp = self.health
        self.turn = 0
    def damage(self):
        self.turn += 1
        return self.attack

class DrizzleSlime(Monster):
    name, health, attack, xp, gold = 'Drizzle Slime', 30, 6, 15, 12

class GustWolf(Monster):
    name, health, attack, xp, gold = 'Gust Wolf', 45, 9, 20, 16

class HailGolem(Monster):
    name, health, attack, xp, gold = 'Hail Golem', 65, 12, 30, 22

class ThunderWraith(Monster):
    name, health, attack, xp, gold = 'Thunder Wraith', 75, 14, 35, 28
    def damage(self):
        damage = super().damage()
        return damage * 2 if self.turn % 3 == 0 else damage

class TempestKing(Monster):
    name, health, attack, xp, gold = 'Tempest King', 160, 18, 100, 100
    def damage(self):
        return super().damage() + (6 if self.hp < self.health // 2 else 0)
