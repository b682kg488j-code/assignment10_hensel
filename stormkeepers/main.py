"""Run with uv run python main.py from this directory."""
import json
from auth import authenticate
from database import Database
from game import Game
from ui import say

def main():
    db = None
    game = None
    try:
        db = Database()
        say('Welcome to STORMKEEPERS')
        username = authenticate(db)
        if username:
            game = Game(db, username)
            game.run()
    except (EOFError, KeyboardInterrupt):
        if game and db:
            db.save(game.username, game.player)
        say('\nGoodbye. Your character has been saved.' if game else '\nGoodbye.')
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        say(f'Unable to read or save game data: {error}', 'bad')
        say('Keep a backup of data/saves.json. Do not edit it while the game is running.')
    finally:
        if db:
            db.close()

if __name__ == '__main__':
    main()
