import os
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Eliminar la base de datos existente
    if os.path.exists('app/db.sqlite'):
        os.remove('app/db.sqlite')
    
    # Crear una nueva base de datos
    db.create_all()
