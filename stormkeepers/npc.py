"""Five named NPCs with unique dialogue and meaningful roles."""
from quest import interact
from ui import say
NPCS = {
    'E': ('Elder Cirrus', 'The Tempest King stole our seasons. Mira can mend my weather compass.'),
    'M': ('Meteorologist Mira', 'Three cloud shards will calibrate the compass and reveal the summit path.'),
    'A': ('Gardener Alba', 'My rain garden is dying. Two cloud shards could bring it back.'),
    'R': ('Ranger Rowan', 'Clear three roaming spirits and I will pay you for the patrol.'),
    'T': ('Sage Thalia', 'The beacon holds sunlight. Light it before challenging the king. Learn healing rain!'),
}

def talk(player, symbol):
    name, dialogue = NPCS[symbol]
    say(f'{name}: "{dialogue}"')
    interact(player, symbol)
