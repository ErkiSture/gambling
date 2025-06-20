from flask import Flask, request, g, render_template, redirect, url_for, session, flash, get_flashed_messages, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ds2slayer69420'
DATABASE = 'mydb.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""CREATE TABLE IF NOT EXISTS users( 
        id INTEGER PRIMARY KEY, 
        name TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        )""")
    db.commit()
    db.close()



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    db = get_db()
    username = session.get('username')
    rows = db.execute('select * from users').fetchall()
    return render_template('index.html', users=rows, username=username)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        remember_me = 'remember' in request.form
        hashed_password = generate_password_hash(password)

        if not name or not password:
            flash('Username and password cannot be empty', 'error')
        else:   
            db = get_db()
            try:
                db.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, hashed_password))
                db.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Username already taken', 'error')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in session:
        return redirect(url_for('index'))

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
            if remember_me:
                session.permanent = True
            else:
                session.permanent = False
            #flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid password. Please try again', 'error')
            

    return render_template('login.html')

@app.route('/clear_db', methods=["POST"])
def clear_db():
    db = get_db()
    db.execute('DELETE FROM users')
    db.execute('DELETE FROM scores')
    db.commit()
    session.clear()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)


