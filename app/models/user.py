from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import redis_client

class User(UserMixin):
    def __init__(self, username, password=None, role=None):
        self.username = username
        if password:
            self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(f"Password hash for {self.username}: {self.password_hash}")

    def check_password(self, password):
        result = check_password_hash(self.password_hash, password)
        print(f"Password check for {self.username}: {result}")
        return result

    @classmethod
    def get_by_id(cls, user_id):
        user_data = redis_client.hgetall(f"user:{int(user_id)}")  # Convert user_id to int
        if user_data:
            print(f"User data found for ID {user_id}: {user_data}")
            user = cls(user_data[b'username'].decode('utf-8'))
            user.password_hash = user_data[b'password_hash'].decode('utf-8')
            user.role = user_data[b'role'].decode('utf-8')
            user.id = int(user_id)  # Ensure user.id is an int
            return user
        print(f"No user data found for ID {user_id}")
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
        cls.index_username(username, user_id)
        return user

    @classmethod
    def get_by_username(cls, username):
        user_id = redis_client.hget("username_index", username)
        if user_id:
            user_id = int(user_id)  # Convert user_id to int
            print(f"User ID found for username {username}: {user_id}")
            return cls.get_by_id(user_id)
        print(f"No user ID found for username {username}")
        return None

    @classmethod
    def index_username(cls, username, user_id):
        redis_client.hset("username_index", username, user_id)

    @classmethod
    def get_all(cls):
        user_ids = redis_client.keys("user:*")
        users = []
        for user_id in user_ids:
            user = cls.get_by_id(user_id.split(b':')[1].decode('utf-8'))
            if user:
                users.append(user)
        print(f"All users fetched: {[user.username for user in users]}")  # Debug statement
        return users