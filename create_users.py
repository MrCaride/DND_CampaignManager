from app import create_app, db
from app.models.user import User
from app.models.character import Character
from app.models.campaign import Campaign
from app.models.combat import Combat

app = create_app()

with app.app_context():
    db.create_all()
    
    # Crear usuarios
    player_user = User(username='player1', password='password1', role='player')
    master_user = User(username='master1', password='password2', role='master')
    
    db.session.add(player_user)
    db.session.add(master_user)
    db.session.commit()
    
    # Crear personajes
    character1 = Character(name='Aragorn', user_id=player_user.id, race='Human', character_class='Ranger')
    character2 = Character(name='Legolas', user_id=player_user.id, race='Elf', character_class='Archer')
    
    db.session.add(character1)
    db.session.add(character2)
    db.session.commit()
    
    # Crear campañas
    campaign1 = Campaign(name='The Fellowship of the Ring', master_id=master_user.id)
    campaign2 = Campaign(name='The Two Towers', master_id=master_user.id)
    
    db.session.add(campaign1)
    db.session.add(campaign2)
    db.session.commit()
    
    # Crear combates
    combat1 = Combat(name='Battle of Helm\'s Deep', user_id=master_user.id)
    combat2 = Combat(name='Battle of Pelennor Fields', user_id=master_user.id)
    
    db.session.add(combat1)
    db.session.add(combat2)
    db.session.commit()
    
    print("Datos creados:")
    print("Usuarios:")
    print("Username: player1, Password: password1, Role: player")
    print("Username: master1, Password: password2, Role: master")
    print("Personajes:")
    print("Name: Aragorn, Race: Human, Class: Ranger")
    print("Name: Legolas, Race: Elf, Class: Archer")
    print("Campañas:")
    print("Name: The Fellowship of the Ring")
    print("Name: The Two Towers")
    print("Combates:")
    print("Name: Battle of Helm's Deep")
    print("Name: Battle of Pelennor Fields")
