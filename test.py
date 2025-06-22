import sqlite3
db = sqlite3.connect('mydb.db')
db.row_factory = sqlite3.Row

""""
CREATE TABLE IF NOT EXISTS friends( 
id INTEGER PRIMARY KEY AUTOINCREMENT, 
user_id INTEGER NOT NULL,
friend_id NOT NULL,
status TEXT NOT NULL CHECK(status IN ('pending', 'accepted')),

UNIQUE(user_id, friend_id)
FOREIGN KEY(user_id) REFERENCES users(id)
FOREIGN KEY(friend_id) REFERENCES users(id)
"""

db.executemany("""
    INSERT INTO gambles (total_money, tip, deviation, group_id, receiver_id)
    VALUES (?, ?, ?, ?, ?)
""", [
    (400, 0, 3.5, 1, 3),
    (500, 10, 2.1, 2, 2),
    (300, 5, 4.2, 4, 1),
])
db.commit()



db.executemany(
    """
    INSERT INTO rolls (gamble_id, roll, random_val, player)
    VALUES (?, ?, ?, ?)
    """,
    [
        (1, 1, -6, 3),
        (1, 2, 4, 2),
        (1, 3, 2, 6),
        (2, 1, -14, 1),
        (2, 2, 10, 2),
        (2, 3, 0, 3)
    ]
)
#db.execute('DELETE FROM gambles')
#db.execute('DELETE FROM rolls')
db.commit()


db.row_factory = None
rows = db.execute('SELECT * FROM gambles').fetchall()
for row in rows:
    print(row)


rows = db.execute('SELECT * FROM rolls').fetchall()
for row in rows:
    print(row)