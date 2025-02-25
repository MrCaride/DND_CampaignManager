from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from redis import Redis
import redis

db = SQLAlchemy()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['REDIS_URL'] = 'redis://localhost:6379/0'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Agrega esta línea para suprimir la advertencia

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Redis
    redis = Redis.from_url(app.config['REDIS_URL'])

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models.user import User  # Importa el modelo User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint  # Asegúrate de que la importación sea correcta
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .routes.characters import characters_bp as characters_blueprint
    from .routes.campaigns import campaigns_bp as campaigns_blueprint
    from .routes.combats import combats_bp as combats_blueprint
    from .routes import main as main_blueprint  # Importa el blueprint principal

    app.register_blueprint(characters_blueprint, url_prefix='/characters')
    app.register_blueprint(campaigns_blueprint, url_prefix='/campaigns')
    app.register_blueprint(combats_blueprint, url_prefix='/combats')
    app.register_blueprint(main_blueprint)  # Registra el blueprint principal

    @app.route('/')
    def index():
        return render_template('index.html')

    return app