"""Buy consumables without allowing negative gold or invalid purchases."""
from item import ITEMS
from inventory import add
from ui import say

def buy(player, item):
    if item not in ITEMS or ITEMS[item]['price'] <= 0:
        say('Choose a healing item from the shop.', 'bad')
        return False
    price = ITEMS[item]['price']
    if player.gold < price:
        say('Not enough gold.', 'bad')
        return False
    player.gold -= price
    add(player, item)
    say('Purchased ' + ITEMS[item]['name'], 'good')
    return True

def visit(player):
    say(f'Gold: {player.gold}', 'gold')
    for key, item in ITEMS.items():
        if item['price']:
            say(f'{key}: {item["price"]} gold, heals {item["heal"]} HP')
    item = input('Buy item ID or back: ').strip().lower()
    if item != 'back':
        buy(player, item)
