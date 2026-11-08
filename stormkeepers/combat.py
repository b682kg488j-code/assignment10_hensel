"""Turn-based battle. Invalid actions do not spend a turn."""
import random
from inventory import add, use, show
from skill import SKILLS
from ui import say

def battle(player, enemy, rng=None):
    rng = rng or random
    cooldowns = {key: 0 for key in player.skills}
    player.shield = 0
    say(f'A {enemy.name} appears!', 'bad')
    while enemy.hp > 0 and player.hp > 0:
        say(f'You: {player.hp}/{player.max_hp} HP | {enemy.name}: {enemy.hp} HP')
        say('Skills: ' + ', '.join(f'{k} (wait {v})' for k, v in cooldowns.items()))
        action = input('attack / skill ID / item / flee: ').strip().lower()
        used_skill = None
        if action == 'attack':
            enemy.hp -= player.attack
            say(f'You deal {player.attack} damage.')
        elif action in cooldowns:
            if cooldowns[action]:
                say('That skill is cooling down.', 'bad')
                continue
            skill = SKILLS[action]()
            say(skill.apply(player, enemy), 'good')
            used_skill = action
        elif action == 'item':
            show(player)
            if not use(player, input('Item ID: ').strip().lower()):
                continue
        elif action == 'flee':
            from monster import TempestKing
            if isinstance(enemy, TempestKing):
                say('The king seals the exit!', 'bad')
                continue
            if rng.random() < 0.65:
                player.shield = 0
                say('You escaped.')
                return 'fled'
            say('Escape failed!', 'bad')
        else:
            say('Invalid battle action.', 'bad')
            continue
        for key in cooldowns:
            cooldowns[key] = max(0, cooldowns[key] - 1)
        if used_skill:
            cooldowns[used_skill] = SKILLS[used_skill].cooldown
        if enemy.hp > 0:
            damage = enemy.damage()
            if player.shield:
                damage = max(1, damage // 2)
                player.shield -= 1
            player.hp = max(0, player.hp - damage)
            say(f'{enemy.name} hits for {damage}.', 'bad')
    player.shield = 0
    if player.hp == 0:
        player.gold = max(0, player.gold - 10)
        player.hp = player.max_hp
        player.map_name, player.x, player.y = 'valley', 1, 1
        say('Rescued by the valley healers. You lose up to 10 gold; quests are kept.', 'bad')
        return 'lost'
    player.kills += 1
    player.gold += enemy.gold
    player.gain_xp(enemy.xp)
    add(player, 'cloud_shard')
    if rng.random() < 0.35:
        add(player, 'rainwater')
        say('Found a rainwater flask!', 'good')
    say(f'Victory! +{enemy.gold} gold, +{enemy.xp} XP, +1 cloud shard.', 'gold')
    return 'won'
