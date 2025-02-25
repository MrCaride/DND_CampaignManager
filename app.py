from flask import Flask
from flask_login import LoginManager
from redis import Redis

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['REDIS_URL'] = 'redis://localhost:6379/0'

    # Initialize Redis
    redis = Redis.from_url(app.config['REDIS_URL'])

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.routes.auth import auth as auth_blueprint
    from app.routes.characters import characters as characters_blueprint
    from app.routes.campaigns import campaigns as campaigns_blueprint
    from app.routes.combats import combats as combats_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(characters_blueprint)
    app.register_blueprint(campaigns_blueprint)
    app.register_blueprint(combats_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)