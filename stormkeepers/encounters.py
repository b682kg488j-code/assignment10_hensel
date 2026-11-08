"""Visible map monsters and chance discoveries on ordinary walking tiles."""
import random
from monster import DrizzleSlime, GustWolf, HailGolem, ThunderWraith
from inventory import add
from combat import battle
from ui import say

# Coordinates are (x, y). These overlays never replace walls or landmarks.
SPAWNS = {
    'valley': {(4, 2): ('1', DrizzleSlime), (11, 2): ('2', GustWolf)},
    'summit': {(4, 3): ('3', HailGolem), (10, 5): ('4', ThunderWraith)},
}

def spawn_key(player):
    return f'{player.map_name}:{player.x}:{player.y}'

def visible_monster(player, x=None, y=None):
    x = player.x if x is None else x
    y = player.y if y is None else y
    key = f'{player.map_name}:{x}:{y}'
    if key in player.cleared_monsters:
        return None
    return SPAWNS[player.map_name].get((x, y))

def fight_visible(player):
    spawn = visible_monster(player)
    if not spawn:
        return
    key = spawn_key(player)  # Defeat may move the player back to camp.
    if battle(player, spawn[1]()) == 'won':
        player.cleared_monsters.append(key)
        say('This monster has been cleared from the map.', 'good')


def walking_event(player, rng=None):
    """A 20% chance per ordinary step; one event at most, never on landmarks."""
    rng = rng or random
    if rng.random() >= 0.20:
        return
    event = rng.choice(['gold', 'item', 'traveler', 'spirit'])
    if event == 'gold':
        amount = rng.randint(5, 12)
        player.gold += amount
        say(f'A gust uncovers a lost purse: +{amount} gold!', 'gold')
    elif event == 'item':
        add(player, 'rainwater')
        say('You stumble upon a rainwater flask beneath a leaf.', 'good')
    elif event == 'traveler':
        player.hp = min(player.max_hp, player.hp + 20)
        say('Wandering forecaster: "Fair winds, friend! Take this warming tea."')
        say('The tea restores up to 20 HP.', 'good')
    else:
        say('A sudden squall reveals a roaming spirit!', 'bad')
        pool = [DrizzleSlime, GustWolf] if player.map_name == 'valley' else [HailGolem, ThunderWraith]
        battle(player, rng.choice(pool)())
