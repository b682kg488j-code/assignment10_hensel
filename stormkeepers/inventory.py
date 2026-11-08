"""Item management used by shops, rewards, and combat."""
from item import ITEMS
from ui import say

def add(player, item, amount=1):
    player.inventory[item] = player.inventory.get(item, 0) + amount

def use(player, item):
    if item not in ITEMS or player.inventory.get(item, 0) <= 0:
        say('You do not have that item.', 'bad')
        return False
    if not ITEMS[item]['heal']:
        say('Keep this for a quest.', 'bad')
        return False
    if player.hp == player.max_hp:
        say('You are already at full health.', 'bad')
        return False
    player.inventory[item] -= 1
    player.hp = min(player.max_hp, player.hp + ITEMS[item]['heal'])
    say(f'Health restored: {player.hp}/{player.max_hp}', 'good')
    return True

def show(player):
    for key, amount in player.inventory.items():
        if amount:
            say(f'{key}: {ITEMS[key]["name"]} x{amount}')
