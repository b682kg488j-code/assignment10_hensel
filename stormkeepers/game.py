"""Overworld command loop connects the independent game systems."""
import random
from player import Player
from world import draw, move, tile
from npc import NPCS, talk
from quest import show as show_quests, interact
from inventory import show as show_inventory, use
from shop import visit
from skill import SKILLS
from monster import DrizzleSlime, GustWolf, HailGolem, ThunderWraith, TempestKing
from combat import battle
from ui import say
from encounters import visible_monster, fight_visible, walking_event

INTRO = '''STORMKEEPERS: THE STOLEN SEASONS
Rain falls upward. Snow burns the fields. Above the broken valley,
the Tempest King has chained the four winds to his crown.
You are the last apprentice Stormkeeper. Gather the scattered cloud
shards, rekindle the summit beacon, and return balance to the sky.'''
HELP = '''AVAILABLE ACTIONS
w/a/s/d: walk up/left/down/right | map: show map | help: show this menu
stats: view HP, XP, level, gold and skills | inventory: view your items
quests: view main and side quest progress | learn: learn weather skills
use: choose a healing item | hunt: seek a roaming monster
rest: heal at valley camp (1,1) | save: save progress | quit: save and exit
interact: repeat the interaction at your current landmark
Step onto people, shops, beacons, monsters, or passages to interact automatically.
Walking on open ground has a 20% chance of a discovery or encounter.
Numbered monsters stay cleared after victory. Camp heals you when you return.
Progress autosaves after commands.'''

class Game:
    def __init__(self, db, username):
        self.db, self.username = db, username
        self.player = db.load(username)
        if self.player is None:
            say(INTRO)
            self.player = Player(username)
            db.save(username, self.player)

    def learn(self):
        p = self.player
        for key, cls in SKILLS.items():
            say(f'{key}: level {cls.level}, cooldown {cls.cooldown} turns' +
                (' (learned)' if key in p.skills else ''))
        key = input('Skill ID or back: ').strip().lower()
        if key == 'back':
            return
        if key not in SKILLS:
            say('Unknown skill.', 'bad')
        elif key in p.skills:
            say('Already learned.')
        elif p.level < SKILLS[key].level:
            say('Reach the required level first.', 'bad')
        else:
            p.skills.append(key)
            say('Skill learned!', 'good')

    def landmark(self):
        p = self.player
        symbol = tile(p)
        if symbol in NPCS:
            talk(p, symbol)
        elif symbol == 'S':
            visit(p)
        elif symbol == 'H':
            interact(p, symbol)
        elif symbol == '>':
            if p.quest < 2:
                say('The storm blocks the pass. Help Mira first.', 'bad')
            else:
                p.map_name, p.x, p.y = 'summit', 1, 1
        elif symbol == '<':
            p.map_name, p.x, p.y = 'valley', 10, 5
        elif symbol == 'B':
            if p.quest == 3:
                if battle(p, TempestKing()) == 'won':
                    p.quest = 4
                    say('YOU WIN! The crown shatters. Gentle rain returns to the valley.', 'good')
                    say('Your victory is saved. You may explore or quit.')
            elif p.quest == 4:
                say('Sunlight fills the empty throne. Your journey is complete.')
            else:
                say('Light the summit beacon before facing the king.', 'bad')
        else:
            say('No landmark here. Use map to find one.')

    def arrive(self):
        """Resolve one arrival only, so travel cannot bounce between portals."""
        p = self.player
        symbol = tile(p)
        if visible_monster(p):
            fight_visible(p)
        elif symbol in NPCS or symbol in ('S', 'H', 'B', '>', '<'):
            self.landmark()
        elif (p.map_name, p.x, p.y) == ('valley', 1, 1):
            p.hp = p.max_hp
            say('You reach camp and rest. Full health.', 'good')
        else:
            walking_event(p)

    def run(self):
        draw(self.player)
        say(HELP)
        while True:
            command = input('\nStormkeeper > ').strip().lower()
            p = self.player
            if command == 'quit':
                self.db.save(self.username, p)
                say('Game saved. May fair winds guide you!')
                return
            if command in ('w', 'a', 's', 'd'):
                if move(p, command):
                    self.arrive()
            elif command == 'map': draw(p)
            elif command == 'interact': self.landmark()
            elif command == 'stats': p.show()
            elif command == 'inventory': show_inventory(p)
            elif command == 'quests': show_quests(p)
            elif command == 'learn': self.learn()
            elif command == 'use': use(p, input('Item ID: ').strip().lower())
            elif command == 'hunt':
                enemies = [DrizzleSlime, GustWolf] if p.map_name == 'valley' else [HailGolem, ThunderWraith]
                battle(p, random.choice(enemies)())
            elif command == 'rest':
                if (p.map_name, p.x, p.y) == ('valley', 1, 1):
                    p.hp = p.max_hp
                    say('You rest beside the campfire. Full health.', 'good')
                else:
                    say('Rest at the valley camp: (1,1).')
            elif command == 'help': say(HELP)
            elif command == 'save': say('Progress saved.', 'good')
            else: say('Unknown command. Type help.', 'bad')
            self.db.save(self.username, p)
            if command in ('w', 'a', 's', 'd', 'interact', 'hunt'):
                draw(p)
                say(HELP)
