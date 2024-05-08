from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes import auth, contact, application, activity, task, note
    app.register_blueprint(auth.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(application.bp)
    app.register_blueprint(activity.bp)
    app.register_blueprint(task.bp)
    app.register_blueprint(note.bp)

    return app
