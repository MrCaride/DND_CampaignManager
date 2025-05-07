from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/operations')
@login_required
def operations():
    print(f"Redirecting user {current_user.username} with role {current_user.role}")
    if current_user.role == 'master':
        return redirect(url_for('main.operations_master'))
    else:
        return redirect(url_for('main.operations_player'))

@main.route('/operations_master')
@login_required
def operations_master():
    return render_template('operations_master.html')

@main.route('/operations_player')
@login_required
def operations_player():
    return render_template('operations_player.html')
