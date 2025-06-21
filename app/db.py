from flask import g, current_app
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = sqlite3.connect(app.config['DATABASE'])
        db.execute("""CREATE TABLE IF NOT EXISTS users( 
            id INTEGER PRIMARY KEY, 
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS friends( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER NOT NULL,
            friend_id NOT NULL,
            sender_id NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'accepted')),
            
            UNIQUE(user_id, friend_id)
            FOREIGN KEY(user_id) REFERENCES users(id)
            FOREIGN KEY(friend_id) REFERENCES users(id)
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS gambles( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            total_money INTEGER NOT NULL,
            tip INTEGER NOT NULL,
            deviation REAL NOT NULL,
            group_id INTEGER,
            date TEXT DEFAULT (DATE('now'))

 
        )""")
        db.commit()
        db.close()