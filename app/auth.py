from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if not name or not password:
            flash('Username and password cannot be empty', 'error')
        else:
            db = get_db()
            try:
                db.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, hashed_password))
                db.commit()
                return redirect(url_for('auth.login'))
            except Exception:
                flash('Username already taken', 'error')

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        remember_me = 'remember' in request.form

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()
        if user is None:
            flash('Username not found. Please try again', 'error')
        elif check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['name']
            session['logged_in'] = True
            session.permanent = remember_me
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid password. Please try again', 'error')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))