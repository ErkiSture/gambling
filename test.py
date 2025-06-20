import sqlite3
db = sqlite3.connect('mydb.db')
def add_friend(user_id, friend_id):
    if user_id == friend_id:
        return
    if user_id > friend_id:
        user_id, friend_id = friend_id, user_id
    
    try:
        db.execute(
            'INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, ?)',
            (user_id, friend_id, 'pending')
        )
        db.commit()
    except sqlite3.IntegrityError:
        # Handle duplicate or error
        pass
    
add_friend(7, 8)

rows = db.execute('SELECT * FROM friends').fetchall()
for row in rows:
    print(row)
print('-------------')
rows = db.execute('SELECT * FROM friends WHERE friend_id = ? or user_id = ?' , (3, 3,)).fetchall()
for row in rows:
    print(row)

#db.execute('DELETE FROM friends')
#db.commit()

db.close()


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