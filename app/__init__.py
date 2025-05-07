from flask import Flask, render_template
from flask_login import LoginManager
import sirope

# Create Sirope instance
db = sirope.Sirope()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        print(f"Loading user with ID {user_id}")
        return User.get_by_id(user_id)

    # Importar y registrar blueprints
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .routes.characters import characters_bp
    from .routes.campaigns import campaigns_bp
    from .routes.missions import missions_bp
    from .routes import main

    app.register_blueprint(characters_bp, url_prefix='/characters')
    app.register_blueprint(campaigns_bp, url_prefix='/campaigns')
    app.register_blueprint(missions_bp, url_prefix='/missions')
    app.register_blueprint(main)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app