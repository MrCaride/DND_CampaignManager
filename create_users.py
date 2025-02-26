from app import create_app, db
from app.models.user import User
from app.models.character import Character
from app.models.campaign import Campaign
from app.models.mission import Mission
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
    user4 = User(username='user4', password='password4', role='player')
    user5 = User(username='user5', password='password5', role='player')
    master = User(username='master', password='masterpass', role='master')
    master2 = User(username='master2', password='masterpass2', role='master')
    master3 = User(username='master3', password='masterpass3', role='master')

    db.session.add_all([user1, user2, user3, user4, user5, master, master2, master3])
    db.session.commit()

    # Create generic campaigns
    campaign1 = Campaign(name='La comunidad del anillo', master_id=master.id, is_public=True)
    campaign2 = Campaign(name='Las dos torres', master_id=master.id, is_public=False)
    campaign3 = Campaign(name='El retorno del rey', master_id=master.id, is_public=True)
    campaign4 = Campaign(name='La amenaza fantasma', master_id=master.id, is_public=False)
    campaign5 = Campaign(name='El ataque de los clones', master_id=master.id, is_public=True)
    campaign6 = Campaign(name='Raiders of the Lost Ark', master_id=master2.id, is_public=True)
    campaign7 = Campaign(name='The Last Crusade', master_id=master3.id, is_public=False)
    
    campaign2.allowed_players.extend([user1, user2])
    campaign4.allowed_players.extend([user3, user4])
    campaign7.allowed_players.extend([user1, user3])

    db.session.add_all([campaign1, campaign2, campaign3, campaign4, campaign5, campaign6, campaign7])
    db.session.commit()

    # Create characters
    character1 = Character(name='Aragorn', user_id=user1.id, race='Human', character_class='Ranger', hit_points=100, bonus='5', initiative=10)
    character2 = Character(name='Legolas', user_id=user1.id, race='Elf', character_class='Archer', hit_points=80, bonus='3', initiative=15)
    character3 = Character(name='Gimli', user_id=user2.id, race='Dwarf', character_class='Warrior', hit_points=120, bonus='4', initiative=8)
    character4 = Character(name='Frodo', user_id=user3.id, race='Hobbit', character_class='Thief', hit_points=60, bonus='2', initiative=12)
    character5 = Character(name='Luke Skywalker', user_id=user4.id, race='Human', character_class='Jedi', hit_points=90, bonus='6', initiative=14)
    character6 = Character(name='Darth Vader', user_id=user5.id, race='Human', character_class='Sith', hit_points=110, bonus='7', initiative=9)

    db.session.add_all([character1, character2, character3, character4, character5, character6])
    db.session.commit()

    # Create missions
    mission1 = Mission(name='Protect the Shire', description='Ensure the safety of the Shire.', campaign_id=campaign1.id, rewards='100 gold')
    mission2 = Mission(name='Defend Helm\'s Deep', description='Defend the fortress of Helm\'s Deep.', campaign_id=campaign2.id, rewards='200 gold')
    mission3 = Mission(name='Destroy the One Ring', description='Take the One Ring to Mount Doom and destroy it.', campaign_id=campaign3.id, rewards='300 gold')
    mission4 = Mission(name='Negotiate with the Gungans', description='Form an alliance with the Gungans.', campaign_id=campaign4.id, rewards='150 gold')
    mission5 = Mission(name='Battle of Geonosis', description='Fight in the Battle of Geonosis.', campaign_id=campaign5.id, rewards='250 gold')
    mission6 = Mission(name='Find the Ark of the Covenant', description='Locate and retrieve the Ark of the Covenant.', campaign_id=campaign6.id, rewards='500 gold')
    mission7 = Mission(name='Rescue Henry Jones Sr.', description='Rescue Indiana\'s father from the Nazis.', campaign_id=campaign7.id, rewards='400 gold')

    db.session.add_all([mission1, mission2, mission3, mission4, mission5, mission6, mission7])
    db.session.commit()

    # Create combats
    combat1 = Combat(name='Battle of Helm\'s Deep', campaign_id=campaign2.id)
    combat2 = Combat(name='Battle of Pelennor Fields', campaign_id=campaign2.id)
    combat3 = Combat(name='Duel on Mustafar', campaign_id=campaign4.id)
    combat4 = Combat(name='Battle of Endor', campaign_id=campaign5.id)
    combat5 = Combat(name='Battle of Hoth', campaign_id=campaign5.id)
    combat6 = Combat(name='Fight in the Temple of Doom', campaign_id=campaign6.id)
    combat7 = Combat(name='Battle at the Canyon of the Crescent Moon', campaign_id=campaign7.id)

    db.session.add_all([combat1, combat2, combat3, combat4, combat5, combat6, combat7])
    db.session.commit()

    print("Database has been reset and populated with generic data.")
    print("Datos creados:")
    print("Usuarios:")
    print("Username: user1, Password: password1, Role: player")
    print("Username: user2, Password: password2, Role: player")
    print("Username: user3, Password: password3, Role: player")
    print("Username: user4, Password: password4, Role: player")
    print("Username: user5, Password: password5, Role: player")
    print("Username: master, Password: masterpass, Role: master")
    print("Username: master2, Password: masterpass2, Role: master")
    print("Username: master3, Password: masterpass3, Role: master")
    print("Personajes:")
    print("Name: Aragorn, Race: Human, Class: Ranger")
    print("Name: Legolas, Race: Elf, Class: Archer")
    print("Name: Gimli, Race: Dwarf, Class: Warrior")
    print("Name: Frodo, Race: Hobbit, Class: Thief")
    print("Name: Luke Skywalker, Race: Human, Class: Jedi")
    print("Name: Darth Vader, Race: Human, Class: Sith")
    print("Campañas:")
    print("Name: La comunidad del anillo")
    print("Name: Las dos torres")
    print("Name: El retorno del rey")
    print("Name: La amenaza fantasma")
    print("Name: El ataque de los clones")
    print("Name: Raiders of the Lost Ark")
    print("Name: The Last Crusade")
    print("Misiones:")
    print("Name: Protect the Shire")
    print("Name: Defend Helm's Deep")
    print("Name: Destroy the One Ring")
    print("Name: Negotiate with the Gungans")
    print("Name: Battle of Geonosis")
    print("Name: Find the Ark of the Covenant")
    print("Name: Rescue Henry Jones Sr.")
    print("Combates:")
    print("Name: Battle of Helm's Deep")
    print("Name: Battle of Pelennor Fields")
    print("Name: Duel on Mustafar")
    print("Name: Battle of Endor")
    print("Name: Battle of Hoth")
    print("Name: Fight in the Temple of Doom")
    print("Name: Battle at the Canyon of the Crescent Moon")
