from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sirope import OID

class User(UserMixin):
    def __init__(self, username, password=None, role=None, _id=None):
        self.username = username
        self.role = role
        self._id = _id  # Initialize _id in constructor
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(f"Password hash for {self.username}: {self.password_hash}")

    def check_password(self, password):
        result = check_password_hash(self.password_hash, password)
        print(f"Password check for {self.username}: {result}")
        return result

    @property
    def id(self):
        return str(self._id) if self._id else None

    @classmethod
    def get_by_id(cls, user_id):
        try:
            # En Sirope, buscamos por el OID
            oid = OID.from_str(user_id)
            user = db.load(oid)
            if isinstance(user, cls):
                return user
        except:
            pass
        return None

    @classmethod
    def create(cls, username, password, role):
        user = cls(username, password, role)
        # Guardamos el usuario en Sirope y obtenemos su OID
        oid = db.save(user)
        user._id = oid
        return user

    @classmethod
    def get_by_username(cls, username):
        print(f"Searching for user with username: {username}")
        try:
            # Obtener todos los usuarios primero para debug
            all_users = list(db.load_all(cls))
            print(f"All users in database: {[u.username for u in all_users]}")
            
            # En Sirope, usamos find_first para buscar por username
            user = db.find_first(cls, lambda u: hasattr(u, 'username') and u.username == username)
            if user:
                print(f"Found user: {user.username} with role: {user.role}")
            else:
                print(f"No user found with username: {username}")
            return user
        except Exception as e:
            print(f"Error searching for user: {str(e)}")
            return None

    @classmethod
    def get_all(cls):
        # En Sirope, usamos load_all para obtener todos los usuarios
        return list(db.load_all(cls))