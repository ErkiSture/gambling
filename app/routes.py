from flask import Blueprint, render_template, session, redirect, url_for, request
from .db import get_db

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
def index():
    db = get_db()
    username = session.get('username')
    rows = db.execute('SELECT * FROM users').fetchall()
    return render_template('index.html', users=rows, username=username)

@bp.route('/clear_db', methods=["POST"])
def clear_db():
    db = get_db()
    db.execute('DELETE FROM users')
    db.execute('DELETE FROM scores')
    db.commit()
    session.clear()
    return redirect(url_for('routes.index'))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
 

@bp.route('/friends')
def friends():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    db = get_db()
    user_id = session.get('user_id')
    #print(user_id)
    friends = db.execute('SELECT * FROM friends WHERE friend_id = ? or user_id = ?' , (user_id, user_id,)).fetchall()
    friends_table = db.execute('SELECT * FROM friends').fetchall()
    return render_template('friends.html', friends=friends, friends_table=friends_table)


def add_friendship_to_db(user_id, friend_id):
    print(user_id, friend_id, 'AAAAAAAAAA')
    if user_id > friend_id:
        user_id, friend_id = friend_id, user_id

    db = get_db()
    db.execute('INSERT INTO friends (user_id, friend_id, status) VALUES (?, ?, ?)', (user_id, friend_id, 'pending'))
    db.commit()
    print('perhaps friends now?')

@bp.route('/add_friend', methods=["POST"])
def add_friend():
    friend_name = request.form['friend_name']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE name = ?', (friend_name,)).fetchone()
    if user is None:
        return "User doesn't exist"
    
    if user['name'] == session['username']:
        return "You can't be friends with yourself"
    friend_id = user['id']

    pair_already_exists = db.execute(
        '''SELECT 1 FROM friends
        WHERE (user_id = ? AND friend_id = ?)
            OR (user_id = ? AND friend_id = ?)''',
        (session['user_id'], friend_id, friend_id, session['user_id'])
        ).fetchone()
    if pair_already_exists:
        return 'You already friends or pending type shit'   

    print(friend_name, friend_id, session['user_id'], session['username'])
    add_friendship_to_db(session['user_id'], friend_id)
    
    return redirect(url_for('routes.friends'))
