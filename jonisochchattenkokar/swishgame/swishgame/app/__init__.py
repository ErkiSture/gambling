from flask import Flask
from .db import init_db
from .routes import game_bp

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = 'swish.db'

    # Initiera databas om den inte finns
    with app.app_context():
        init_db()

    # Registrera routes
    app.register_blueprint(game_bp)

    return app