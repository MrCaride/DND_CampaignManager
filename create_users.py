from app import create_app, db
from app.models.user import User
from app.models.character import Character
from app.models.campaign import Campaign
from app.models.combat import Combat

app = create_app()

with app.app_context():
    # Reset the database
    db.drop_all()
    db.create_all()

    # Create generic users
    user1 = User(username='user1', password='password1', role='player')
    user2 = User(username='user2', password='password2', role='player')
    user3 = User(username='user3', password='password3', role='player')
    master = User(username='master', password='masterpass', role='master')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(master)
    db.session.commit()

    # Create generic campaigns
    campaign1 = Campaign(name='La comunidad del anillo', master_id=master.id, is_public=True)
    campaign2 = Campaign(name='Las dos torres', master_id=master.id, is_public=False, allowed_players=[user1.id, user2.id])

    db.session.add(campaign1)
    db.session.add(campaign2)
    db.session.commit()

    # Crear personajes
    character1 = Character(name='Aragorn', user_id=user1.id, race='Human', character_class='Ranger')
    character2 = Character(name='Legolas', user_id=user1.id, race='Elf', character_class='Archer')

    db.session.add(character1)
    db.session.add(character2)
    db.session.commit()

    # Crear combates
    combat1 = Combat(name='Battle of Helm\'s Deep', user_id=master.id)
    combat2 = Combat(name='Battle of Pelennor Fields', user_id=master.id)

    db.session.add(combat1)
    db.session.add(combat2)
    db.session.commit()

    print("Database has been reset and populated with generic data.")
    print("Datos creados:")
    print("Usuarios:")
    print("Username: user1, Password: password1, Role: player")
    print("Username: user2, Password: password2, Role: player")
    print("Username: user3, Password: password3, Role: player")
    print("Username: master, Password: masterpass, Role: master")
    print("Personajes:")
    print("Name: Aragorn, Race: Human, Class: Ranger")
    print("Name: Legolas, Race: Elf, Class: Archer")
    print("Campañas:")
    print("Name: La comunidad del anillo")
    print("Name: Las dos torres")
    print("Combates:")
    print("Name: Battle of Helm's Deep")
    print("Name: Battle of Pelennor Fields")
