import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from .config import config_by_name

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_name='default'):
    """App factory method"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    # Auth Blueprint
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    # Main Blueprint (Dashboard, Profile)
    from app.main.routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    # Journal Blueprint
    from app.journal.routes import journal_bp
    app.register_blueprint(journal_bp, url_prefix='/')

    # Social Blueprint
    from app.social.routes import social_bp
    app.register_blueprint(social_bp, url_prefix='/')

    # Fitness Blueprint
    from app.fitness.routes import fitness_bp
    app.register_blueprint(fitness_bp, url_prefix='/')

    @app.shell_context_processor
    def make_shell_context():
        from app.models.user import User
        # Include future models here
        return {
            'db': db,
            'User': User
        }

    return app

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))
