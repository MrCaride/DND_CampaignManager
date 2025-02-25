from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Agrega el campo role

    def __init__(self, username, password, role):
        self.username = username
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_by_id(cls, user_id):
        user_data = redis_client.hgetall(f"user:{user_id}")
        if user_data:
            user = cls(user_data['username'], user_data['password_hash'], user_data['role'])
            user.id = user_id
            return user
        return None

    @classmethod
    def create(cls, username, password, role):
        user = cls(username, password, role)
        user_id = redis_client.incr("user_id")  # Increment user ID
        user.id = user_id
        redis_client.hmset(f"user:{user_id}", {
            "username": username,
            "password_hash": user.password_hash,
            "role": role
        })
        return user

    @classmethod
    def get_by_username(cls, username):
        user_id = redis_client.hget("username_index", username)
        if user_id:
            return cls.get_by_id(user_id)
        return None

    @classmethod
    def index_username(cls, username, user_id):
        redis_client.hset("username_index", username, user_id)