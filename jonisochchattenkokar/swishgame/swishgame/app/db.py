import sqlite3
from flask import current_app, g
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT,
            roll INTEGER,
            pengar_i_spel INTEGER,
            dricks INTEGER,
            avvikelse INTEGER,
            grupp_id TEXT,
            spelare TEXT,
            mottagare TEXT,
            slumptal INTEGER,
            datum_tid TEXT
        )
    ''')
    db.commit()