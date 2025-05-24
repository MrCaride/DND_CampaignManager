from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt for username: {username}")
        
        user = User.get_by_username(username)
        if user and user.get_id():  # Verificar que el usuario tenga ID usando get_id()
            print(f"User found: {user.username}, ID: {user.get_id()}")
            if user.check_password(password):
                print("Password verified successfully")
                try:
                    if login_user(user, remember=True):  # Mantener la sesión
                        print(f"User {user.username} logged in successfully with ID: {user.get_id()}")
                        return redirect(url_for('main.operations'))
                    else:
                        print("Login_user failed")
                except Exception as e:
                    print(f"Error during login: {str(e)}")
            else:
                print("Password verification failed")
        else:
            print(f"No valid user found with username: {username}")
        
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])  
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.get_by_username(username):
            flash('El nombre de usuario ya existe. Por favor elija otro.', 'error')
            return render_template('auth/register.html')
            
        try:
            user = User.create(username, password, role)
            if user and user.get_id():  # Verificar que el usuario tenga ID usando get_id()
                print(f"Created new user with ID: {user.get_id()}")
                if login_user(user, remember=True):  # Mantener la sesión
                    print(f"User {user.username} logged in successfully after registration")
                    flash('Registro exitoso!', 'success')
                    return redirect(url_for('main.operations'))
                else:
                    print("Failed to login after registration")
            else:
                print("User created but no ID assigned")
                flash('Error al crear el usuario', 'error')
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            flash('Error al crear el usuario', 'error')
            
        return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))