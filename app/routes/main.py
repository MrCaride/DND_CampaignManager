from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from app import redis_client

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

# Define operations_master route
@main.route('/operations_master')
@login_required
def operations_master():
    return render_template('operations_master.html')

# Define operations_player route
@main.route('/operations_player')
@login_required
def operations_player():
    return render_template('operations_player.html')

# Test route to check Redis connection
@main.route('/test_redis')
def test_redis():
    try:
        redis_client.set('test_key', 'test_value')
        value = redis_client.get('test_key').decode('utf-8')
        return jsonify({"status": "success", "value": value})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Test route to verify data stored in Redis
@main.route('/verify_data')
def verify_data():
    key = request.args.get('key')
    if not key:
        return jsonify({"status": "error", "message": "Key parameter is required"})
    
    try:
        data = redis_client.hgetall(key)
        if not data:
            return jsonify({"status": "error", "message": f"No data found for key: {key}"})
        
        decoded_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}
        return jsonify({"status": "success", "data": decoded_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Test route to fetch and display user data
@main.route('/user_data/<int:user_id>')
def user_data(user_id):
    try:
        user_key = f"user:{user_id}"
        user_data = redis_client.hgetall(user_key)
        if not user_data:
            return jsonify({"status": "error", "message": f"No data found for user ID: {user_id}"})
        
        decoded_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in user_data.items()}
        return jsonify({"status": "success", "data": decoded_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
