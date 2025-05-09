from flask import Flask, render_template
from flask_login import LoginManager
import sirope
from datetime import timedelta
from sirope import OID

# Create Sirope instance
db = sirope.Sirope()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)  # Duración de la cookie de sesión
    app.config['REMEMBER_COOKIE_SECURE'] = False  # Para desarrollo local
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['SESSION_PROTECTION'] = 'strong'

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        print(f"Loading user with ID {user_id}")
        try:
            # Convertir el string del ID a un OID y cargar el usuario
            if '@' in user_id:
                # Si el ID tiene formato 'app.models.user.User@0', extraer el número
                oid_num = int(user_id.split('@')[-1])
                all_users = list(db.load_all(User))
                # Buscar el usuario con el _oid correspondiente
                for user in all_users:
                    if hasattr(user, '_oid') and user._oid and str(user._oid).endswith(f'@{oid_num}'):
                        print(f"Successfully loaded user: {user.username}")
                        return user
            print(f"No user found with ID: {user_id}")
        except Exception as e:
            print(f"Error in user_loader: {str(e)}")
        return None

    # Importar y registrar blueprints
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .routes.characters import characters_bp
    from .routes.campaigns import campaigns_bp
    from .routes.missions import missions_bp
    from .routes import main

    app.register_blueprint(characters_bp, url_prefix='/characters')
    app.register_blueprint(campaigns_bp, url_prefix='/campaigns')
    app.register_blueprint(missions_bp, url_prefix='')  # Remove the /missions prefix since it's already in the route
    app.register_blueprint(main)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app