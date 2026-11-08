"""Polymorphic skills. Cooldowns count subsequent player turns."""
class Skill:
    name = 'Skill'
    cooldown = 0
    level = 1
    def apply(self, player, enemy):
        raise NotImplementedError

class Lightning(Skill):
    name, cooldown, level = 'Lightning', 2, 1
    def apply(self, player, enemy):
        damage = player.attack + 12
        enemy.hp -= damage
        return f'Lightning strikes for {damage} damage.'

class HealingRain(Skill):
    name, cooldown, level = 'Healing Rain', 3, 2
    def apply(self, player, enemy):
        before = player.hp
        player.hp = min(player.max_hp, player.hp + 32)
        return f'Healing rain restores {player.hp - before} HP.'

class FrostShield(Skill):
    name, cooldown, level = 'Frost Shield', 3, 3
    def apply(self, player, enemy):
        player.shield = 2
        return 'Ice armor halves damage from the next two enemy attacks.'

SKILLS = {'lightning': Lightning, 'healing_rain': HealingRain, 'frost_shield': FrostShield}
