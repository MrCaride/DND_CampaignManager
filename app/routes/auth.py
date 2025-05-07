from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Attempting login with username: {username}")
        user = User.get_by_username(username)
        if user and user.check_password(password):
            print(f"User found and password verified for {username}")
            login_user(user)
            print(f"User {username} logged in successfully with role {user.role}")
            return redirect(url_for('main.operations'))
        else:
            print(f"Login failed for username: {username}")
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    print(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.get_by_username(username):
            flash('Username already exists.', 'danger')
            return render_template('register.html')
            
        user = User.create(username, password, role)
        print(f"Created new user: {username} with role: {role}")
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.operations'))
    return render_template('register.html')