from flask import Blueprint, render_template, session, redirect, url_for, request
from .db import get_db

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
def index():
    db = get_db()
    username = session.get('username')
    rows = db.execute('SELECT * FROM scores').fetchall()
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