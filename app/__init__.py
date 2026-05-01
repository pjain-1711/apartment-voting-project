from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access the admin panel.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes import admin, voting, results

    app.register_blueprint(admin.bp)
    app.register_blueprint(voting.bp)
    app.register_blueprint(results.bp)

    # Create instance folder if it doesn't exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database and seed default data
    with app.app_context():
        from app import models
        db.create_all()

        # Seed default admin user if not exists
        if not models.AdminUser.query.first():
            admin_user = models.AdminUser(
                username=app.config['ADMIN_USERNAME']
            )
            admin_user.set_password(app.config['ADMIN_PASSWORD'])
            db.session.add(admin_user)
            db.session.commit()
            print(f"Default admin user created: {app.config['ADMIN_USERNAME']}")

        # Seed default config settings if not exist
        default_settings = {
            'voting_enabled': 'true',
            'results_visible': 'false',
            'winners_per_gender': '2'
        }
        for key, value in default_settings.items():
            if not models.ConfigSetting.query.filter_by(key=key).first():
                setting = models.ConfigSetting(key=key, value=value)
                db.session.add(setting)
        db.session.commit()

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))
