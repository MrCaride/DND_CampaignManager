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
        
        user = User.get_by_username(username)
        if user and user.get_id():
            if user.check_password(password):
                if login_user(user, remember=True):
                    return redirect(url_for('main.operations'))
                    
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
        if user and user.get_id():
            if login_user(user):
                flash('Registro exitoso!', 'success')
                return redirect(url_for('main.operations'))
            else:
                flash('Error al iniciar sesión después del registro', 'error')
                return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
