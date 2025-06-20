


from flask import g
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
        db.commit()
        db.close()