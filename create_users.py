from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear usuarios
    player_user = User(username='player1', password='password1', role='player')
    master_user = User(username='master1', password='password2', role='master')
    
    db.session.add(player_user)
    db.session.add(master_user)
    db.session.commit()
    
    print("Usuarios creados:")
    print("Username: player1, Password: password1, Role: player")
    print("Username: master1, Password: password2, Role: master")
