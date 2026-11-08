"""Main quest is a monotonic state machine; side flags prevent repeat rewards."""
from inventory import add
from ui import say
STEPS = [
    'Speak to Elder Cirrus (E) in the valley.',
    'Defeat spirits to collect 3 cloud_shards, then speak to Meteorologist Mira (M).',
    'Travel to the summit (>) and activate the weather beacon (H).',
    'Defeat the Tempest King (B) on the summit.',
    'Victory! The seasons are restored.',
]

def show(player):
    say(f'Main quest {min(player.quest + 1, 5)}/5: {STEPS[player.quest]}')
    say('Side: Albas collection (A): ' + ('complete' if player.side['shards'] else 'deliver 2 shards'))
    say('Side: Rangers patrol (R): ' + ('complete' if player.side['patrol'] else f'win 3 battles ({player.kills}/3)'))

def interact(player, symbol):
    if symbol == 'E' and player.quest == 0:
        player.quest = 1
        say('Main quest started: bring Mira three cloud shards.', 'good')
    elif symbol == 'M' and player.quest == 1:
        if player.inventory.get('cloud_shard', 0) >= 3:
            player.inventory['cloud_shard'] -= 3
            player.quest = 2
            player.gain_xp(35)
            say('Mira repairs the compass. The summit passage is open!', 'good')
        else:
            say('Mira needs three cloud shards. Use hunt to find spirits.')
    elif symbol == 'H':
        if player.quest == 2:
            player.quest = 3
            player.hp = player.max_hp
            add(player, 'sunfruit', 2)
            player.gain_xp(40)
            say('Beacon lit! Health restored; two sunfruit received. Face the king.', 'good')
        else:
            say('The beacon hums in the mountain wind.')
    elif symbol == 'A' and not player.side['shards']:
        if player.inventory.get('cloud_shard', 0) >= 2:
            player.inventory['cloud_shard'] -= 2
            player.side['shards'] = True
            player.gold += 35
            add(player, 'sunfruit')
            say('Collection complete: 35 gold and a sunfruit!', 'good')
        else:
            say('Alba needs two cloud shards for her rain garden.')
    elif symbol == 'R' and not player.side['patrol']:
        if player.kills >= 3:
            player.side['patrol'] = True
            player.gold += 30
            player.gain_xp(30)
            say('Patrol complete: 30 gold and 30 XP!', 'good')
        else:
            say('Win three battles, then report to Rowan.')
