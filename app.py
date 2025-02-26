from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
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
    login_manager.login_view = 'auth.login'

    from app.routes.auth import auth_bp as auth_blueprint
    from app.routes.characters import characters_bp as characters_blueprint
    from app.routes.campaigns import campaigns_bp as campaigns_blueprint
    from app.routes.combats import combats_bp as combats_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(characters_blueprint, url_prefix='/characters')
    app.register_blueprint(campaigns_blueprint, url_prefix='/campaigns')
    app.register_blueprint(combats_blueprint, url_prefix='/combats')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('welcome'))
        return render_template('index.html')

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    return app

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)