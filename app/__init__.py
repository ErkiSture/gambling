from flask import Flask
from .db import init_db, close_db
from .routes import bp as routes_bp
from .auth import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ds2slayer69420'
    app.config['DATABASE'] = 'mydb.db'

    init_db(app)
    app.teardown_appcontext(close_db)

    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app