from flask import Blueprint, render_template, session, redirect, url_for, request
from .db import get_db


bp = Blueprint('stats', __name__)

@bp.route('/stats')
def stats():
    db = get_db()
    
    result = db.execute(
    """
    SELECT 
    SUM(random_val) as total_plus_minus,
    count(*) as total_rolls
    FROM rolls
    WHERE player = ?
    """, (session['user_id'],)
    ).fetchone()

    total_plus_minus = result['total_plus_minus'] or 0
    total_rolls = result['total_rolls']

    gambles_table = db.execute('SELECT * FROM gambles').fetchall()
    rolls_table = db.execute('SELECT * FROM rolls').fetchall()


    return render_template(
        'stats.html', 
        total_plus_minus=total_plus_minus, 
        total_rolls=total_rolls, 
        gambles_table=gambles_table,
        rolls_table = rolls_table
    ) 