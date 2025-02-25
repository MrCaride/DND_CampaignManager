import os
from app import create_app, db
from app.models.user import User
from app.models.character import Character
from app.models.campaign import Campaign
from app.models.combat import Combat

app = create_app()

with app.app_context():
    # Eliminar la base de datos existente
    if os.path.exists('app/db.sqlite'):
        os.remove('app/db.sqlite')
        print(f"Base de datos borrada correctamente.")
    
    # Crear una nueva base de datos
    db.create_all()
