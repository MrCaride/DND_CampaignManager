from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user:
            print(f"User found: {user.username}")
            if user.check_password(password):
                print("Password check passed")
                login_user(user)
                print(f"User {user.username} logged in with role {user.role}")
                # Redirect to operations route
                return redirect(url_for('main.operations'))
            else:
                print("Password check failed")
        else:
            print("User not found")
        flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        user = User.create(username, password, role)
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth.route('/register', methods=['GET', 'POST'])  
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        user = User.create(username, password, role)
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    print(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('auth.login'))
