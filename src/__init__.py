from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from src.config import Config
from flask_cors import CORS

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="http://localhost:5173")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    from src.routes.auth import auth_bp
    from src.routes.chat import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    return app
