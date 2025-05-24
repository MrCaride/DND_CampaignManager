from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin):
    def __init__(self, username, password=None, role=None, _id=None):
        self.username = username
        self.role = role
        self._oid = _id  # Usar _oid para almacenar el ID
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Método requerido por Flask-Login"""
        if self._oid:
            # Asegurar que retornamos un string con el formato correcto
            return str(self._oid)
        return None

    def __getstate__(self):
        """Método especial para pickle/Sirope - asegura que el _oid se guarde"""
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """Método especial para pickle/Sirope - asegura que el _oid se restaure"""
        self.__dict__.update(state) 

    @classmethod
    def get_by_id(cls, user_id):
        try:
            if not user_id:
                return None

            # Si el ID tiene formato 'app.models.user.User@0', extraer el número
            if '@' in str(user_id):
                oid_num = int(str(user_id).split('@')[-1])
                all_users = list(db.load_all(cls))
                # Buscar el usuario con el _oid correspondiente
                for user in all_users:
                    if hasattr(user, '_oid') and user._oid and str(user._oid).endswith(f'@{oid_num}'):
                        return user
        except Exception as e:
            pass
        return None

    @classmethod
    def create(cls, username, password, role):
        # Verificar si el usuario ya existe
        existing = cls.get_by_username(username)
        if existing:
            return existing

        user = cls(username, password, role)
        
        # Guardar el usuario y obtener su OID
        oid = db.save(user)
        user._oid = oid
        
        # Volver a guardar para asegurar que el _oid se persiste
        db.save(user)
        return user

    @classmethod
    def get_by_username(cls, username):
        try:
            # Obtener todos los usuarios
            all_users = list(db.load_all(cls))
            
            # Buscar el usuario por username y asegurar que tiene _oid
            for user in all_users:
                if user.username == username:
                    if not hasattr(user, '_oid') or not user._oid:
                        # Si no tiene _oid o es None, obtener uno nuevo
                        oid = db.save(user)
                        user._oid = oid
                        db.save(user)
                    return user
            return None
        except Exception as e:
            return None

    @classmethod
    def get_all(cls):
        """Retorna todos los usuarios"""
        return list(db.load_all(cls))