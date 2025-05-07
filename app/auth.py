from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt for username: {username}")
        print(f"Password received: {password}")
        
        user = User.get_by_username(username)
        if user:
            print(f"User found: {user.username}, role: {user.role}")
            print(f"Stored password hash: {user.password_hash}")
            if user.check_password(password):
                print("Password verified successfully")
                login_user(user)
                print(f"User {user.username} logged in successfully")
                return redirect(url_for('main.operations'))
            else:
                print("Password verification failed")
                print(f"Attempting to verify '{password}' against hash {user.password_hash}")
        else:
            print(f"No user found with username: {username}")
        
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])  
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Verificar si el usuario ya existe
        if User.get_by_username(username):
            flash('El nombre de usuario ya existe. Por favor elija otro.', 'error')
            return render_template('auth/register.html')
            
        user = User.create(username, password, role)
        login_user(user)
        flash('Registro exitoso!', 'success')
        return redirect(url_for('main.operations'))
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    print(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('auth.login'))
