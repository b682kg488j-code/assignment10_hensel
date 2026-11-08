"""Account registration and login using salted PBKDF2 hashes."""
import hashlib
import hmac
import secrets
import re
from getpass import getpass
from ui import choose, say

ITERATIONS = 200_000

def digest(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), ITERATIONS).hex()

def register(db, username, password):
    username = username.strip().lower()
    if not re.fullmatch(r'[a-z0-9_]{3,20}', username):
        raise ValueError('Username must be 3–20 letters, numbers, or underscores.')
    if len(password) < 6:
        raise ValueError('Password must be at least six characters.')
    if db.account(username):
        raise ValueError('That username already exists.')
    salt = secrets.token_hex(16)
    db.accounts.insert({'username': username, 'salt': salt, 'hash': digest(password, salt)})
    return username

def login(db, username, password):
    record = db.account(username.strip().lower())
    return bool(record and hmac.compare_digest(record['hash'], digest(password, record['salt'])))

def authenticate(db):
    while True:
        action = choose('[r]egister / [l]ogin / [q]uit: ', ['r', 'l', 'q'])
        if action == 'q':
            return None
        username = input('Username: ').strip().lower()
        password = getpass('Password (hidden): ')
        if action == 'r':
            try:
                register(db, username, password)
                say('Account created. Welcome, Stormkeeper!', 'good')
                return username
            except ValueError as error:
                say(error, 'bad')
        elif login(db, username, password):
            return username
        else:
            say('Incorrect username or password.', 'bad')
