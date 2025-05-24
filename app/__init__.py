from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
import sirope
from datetime import timedelta
from redis import Redis

# Create Sirope instance
db = sirope.Sirope()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['REMEMBER_COOKIE_SECURE'] = False
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['SESSION_PROTECTION'] = 'strong'
    app.config['REDIS_URL'] = 'redis://localhost:6379/0'

    # Initialize Redis
    redis = Redis.from_url(app.config['REDIS_URL'])

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'
    login_manager.login_message = 'Please log in to access this page.'

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            if '@' in user_id:
                oid_num = int(user_id.split('@')[-1])
                all_users = list(db.load_all(User))
                for user in all_users:
                    if hasattr(user, '_oid') and user._oid and str(user._oid).endswith(f'@{oid_num}'):
                        return user
            return None
        except Exception:
            return None

    # Main routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('main.operations'))
        return render_template('index.html')

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    # Register blueprints
    from .auth import auth
    from .routes.characters import characters_bp
    from .routes.campaigns import campaigns_bp
    from .routes.missions import missions_bp
    from .routes.main import main

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(characters_bp, url_prefix='/characters')
    app.register_blueprint(campaigns_bp, url_prefix='/campaigns')
    app.register_blueprint(missions_bp)
    app.register_blueprint(main)

    return app