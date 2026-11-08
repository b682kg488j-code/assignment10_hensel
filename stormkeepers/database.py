"""TinyDB tables store JSON dictionaries. Password hashes are not plaintext."""
from pathlib import Path
from tinydb import TinyDB, Query

class Database:
    def __init__(self, path=None):
        path = Path(path) if path else Path(__file__).parent / 'data' / 'saves.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(path)
        self.accounts = self.db.table('accounts')
        self.games = self.db.table('games')

    def account(self, username):
        return self.accounts.get(Query().username == username)

    def save(self, username, player):
        self.games.upsert({'username': username, 'version': 1, 'player': player.to_data()},
                          Query().username == username)

    def load(self, username):
        from player import Player
        record = self.games.get(Query().username == username)
        return Player.from_data(record['player']) if record else None

    def close(self):
        self.db.close()
