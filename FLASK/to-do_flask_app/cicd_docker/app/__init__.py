from flask import Flask
from .db import init_db
from .routes import todo_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    init_db()
    app.register_blueprint(todo_bp)
    return app
