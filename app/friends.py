from flask import Blueprint, render_template, session, redirect, url_for, request
from .db import get_db


bp = Blueprint('friends', __name__)

@bp.route('/friends')
def friends():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    db = get_db()
    user_id = session.get('user_id')
    #print(user_id)
    
    friends = db.execute("""SELECT * FROM friends WHERE (friend_id = ? or user_id = ?) AND status = 'accepted'""" , (user_id, user_id,)).fetchall()
    friends_list = []
    for row in friends:
        friend_id = row['friend_id'] if row['user_id'] == session['user_id'] else row['user_id']
        friend = db.execute('SELECT * FROM users where id = ?', (friend_id,)).fetchone()
        friends_list.append(friend)

    incoming_friend_requests = db.execute("""
        SELECT f.*, u.name AS sender_name
        FROM friends f
        JOIN users u ON u.id = f.sender_id
        WHERE f.status = 'pending' AND (f.user_id = ? OR f.friend_id = ?) AND f.sender_id != ?
    """, (user_id, user_id, user_id,)).fetchall()
    friends_table = db.execute('SELECT * FROM friends').fetchall()

    return render_template('friends.html', friends_list=friends_list, friends_table=friends_table, incoming_friend_requests=incoming_friend_requests)


def add_friendship_to_db(user_id, friend_id):
    #print(user_id, friend_id, 'AAAAAAAAAA')
    sender_id = user_id
    if user_id > friend_id:
        user_id, friend_id = friend_id, user_id

    db = get_db()
    db.execute('INSERT INTO friends (user_id, friend_id, sender_id, status) VALUES (?, ?, ?, ?)', (user_id, friend_id, sender_id, 'pending'))
    db.commit()
    #print('perhaps friends now?')

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

    #print(friend_name, friend_id, session['user_id'], session['username'])
    add_friendship_to_db(session['user_id'], friend_id)
    
    return redirect(url_for('friends.friends'))


@bp.route('/respond_friend', methods=['POST'])
def respond_friend():
    request_id = request.form['request_id']
    action = request.form['action']
    print(request_id, action)
    db = get_db()
    #row = db.execute('SELECT * FROM friends WHERE id = ?', (request_id,)).fetchone()
    #print(row['status'])
    if action == 'accept':
        db.execute('UPDATE friends SET status = ? WHERE id = ?', ('accepted', request_id,))
    else:
        db.execute('DELETE FROM friends WHERE id = ?', (request_id,))
    db.commit()
   
    return redirect(url_for('friends.friends'))
    
@bp.route('/remove_friend', methods=['POST'])
def remove_friend():
    friend_id = int(request.form['friend_id'])
    user_id = session['user_id']

    if user_id > friend_id:
        user_id, friend_id = friend_id, user_id
    print(user_id, friend_id)

    db = get_db()
    db.execute('DELETE FROM friends WHERE user_id = ? and friend_id = ?', (user_id, friend_id,))
    db.commit()

    return redirect(url_for('friends.friends'))