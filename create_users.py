from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear usuarios
    user1 = User(username='user1', password='password1')
    user2 = User(username='user2', password='password2')
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    
    print("Usuarios creados:")
    print("Username: user1, Password: password1")
    print("Username: user2, Password: password2")
