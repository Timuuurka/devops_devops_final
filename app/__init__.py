from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Важно: НЕ делаем seed здесь, потому что gunicorn запускает несколько воркеров
    # и seed будет выполняться параллельно -> конфликт UNIQUE.
    with app.app_context():
        from app import models
        db.create_all()

    return app
