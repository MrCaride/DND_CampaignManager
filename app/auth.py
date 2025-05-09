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
            print(f"User ID: {user.get_id()}")  # Usar get_id() en lugar de .id
            print(f"Stored password hash: {user.password_hash}")
            if user.check_password(password):
                print("Password verified successfully")
                # Asegurarse de que login_user reciba el usuario correcto
                login_success = login_user(user)
                print(f"Login success: {login_success}")
                if login_success:
                    print(f"User {user.username} logged in successfully with ID: {user.get_id()}")  # Usar get_id()
                    return redirect(url_for('main.operations'))
                else:
                    print("Login_user failed")
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
        
        if User.get_by_username(username):
            flash('El nombre de usuario ya existe. Por favor elija otro.', 'error')
            return render_template('auth/register.html')
            
        user = User.create(username, password, role)
        if user and user.get_id():  # Verificar que el usuario tiene ID usando get_id()
            print(f"Created new user with ID: {user.get_id()}")  # Usar get_id()
            if login_user(user):
                print(f"User {user.username} logged in successfully after registration")
                flash('Registro exitoso!', 'success')
                return redirect(url_for('main.operations'))
            else:
                print("Failed to login after registration")
                flash('Error al iniciar sesión después del registro', 'error')
                return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    print(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('auth.login'))
