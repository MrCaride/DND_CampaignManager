from app import create_app, redis_client
from app.models.user import User
from app.models.character import Character
from app.models.campaign import Campaign
from app.models.mission import Mission
from app.models.combat import Combat

app = create_app()

def create_initial_users():
    users = [
        {"username": "master", "password": "masterpass", "role": "master"},
        {"username": "player1", "password": "playerpass1", "role": "player"},
        {"username": "player2", "password": "playerpass2", "role": "player"},
    ]

    for user_data in users:
        user = User.create(user_data["username"], user_data["password"], user_data["role"])
        print(f"Created user: {user.username}")

def create_initial_data():
    # Create generic users
    users = [
        {"username": "user1", "password": "password1", "role": "player"},
        {"username": "user2", "password": "password2", "role": "player"},
        {"username": "user3", "password": "password3", "role": "player"},
        {"username": "user4", "password": "password4", "role": "player"},
        {"username": "user5", "password": "password5", "role": "player"},
        {"username": "master2", "password": "masterpass2", "role": "master"},
        {"username": "master3", "password": "masterpass3", "role": "master"},
    ]

    for user_data in users:
        User.create(user_data["username"], user_data["password"], user_data["role"])

    # Create generic campaigns
    campaigns = [
        {"name": "La comunidad del anillo", "master_username": "master", "is_public": True},
        {"name": "Las dos torres", "master_username": "master", "is_public": False, "allowed_players": ["user1", "user2"]},
        {"name": "El retorno del rey", "master_username": "master", "is_public": True},
        {"name": "La amenaza fantasma", "master_username": "master", "is_public": False, "allowed_players": ["user3", "user4"]},
        {"name": "El ataque de los clones", "master_username": "master", "is_public": True},
        {"name": "Raiders of the Lost Ark", "master_username": "master2", "is_public": True},
        {"name": "The Last Crusade", "master_username": "master3", "is_public": False, "allowed_players": ["user1", "user3"]},
    ]

    for campaign_data in campaigns:
        master = User.get_by_username(campaign_data["master_username"])
        campaign = Campaign.create(campaign_data["name"], campaign_data["is_public"], master_id=master.id, allowed_players=campaign_data.get("allowed_players", []))
        print(f"Created campaign: {campaign.name}")

    # Create characters
    characters = [
        {"name": "Aragorn", "user_username": "user1", "race": "Human", "character_class": "Ranger", "level": 10},
        {"name": "Legolas", "user_username": "user1", "race": "Elf", "character_class": "Archer", "level": 8},
        {"name": "Gimli", "user_username": "user2", "race": "Dwarf", "character_class": "Warrior", "level": 12},
        {"name": "Frodo", "user_username": "user3", "race": "Hobbit", "character_class": "Thief", "level": 6},
        {"name": "Luke Skywalker", "user_username": "user4", "race": "Human", "character_class": "Jedi", "level": 14},
        {"name": "Darth Vader", "user_username": "user5", "race": "Human", "character_class": "Sith", "level": 15},
    ]

    for character_data in characters:
        user = User.get_by_username(character_data["user_username"])
        character = Character.create(character_data["name"], character_data["race"], character_data["character_class"], character_data["level"], user.id, user.username)
        print(f"Created character: {character.name} for user: {user.username}")

    # Create missions
    missions = [
        {"name": "Protect the Shire", "description": "Ensure the safety of the Shire.", "campaign_name": "La comunidad del anillo"},
        {"name": "Defend Helm's Deep", "description": "Defend the fortress of Helm's Deep.", "campaign_name": "Las dos torres"},
        {"name": "Destroy the One Ring", "description": "Take the One Ring to Mount Doom and destroy it.", "campaign_name": "El retorno del rey"},
        {"name": "Negotiate with the Gungans", "description": "Form an alliance with the Gungans.", "campaign_name": "La amenaza fantasma"},
        {"name": "Battle of Geonosis", "description": "Fight in the Battle of Geonosis.", "campaign_name": "El ataque de los clones"},
        {"name": "Find the Ark of the Covenant", "description": "Locate and retrieve the Ark of the Covenant.", "campaign_name": "Raiders of the Lost Ark"},
        {"name": "Rescue Henry Jones Sr.", "description": "Rescue Indiana's father from the Nazis.", "campaign_name": "The Last Crusade"},
    ]

    for mission_data in missions:
        campaign = Campaign.get_by_name(mission_data["campaign_name"])
        Mission.create(mission_data["name"], mission_data["description"], mission_data["campaign_name"])
        print(f"Created mission: {mission_data['name']}")

    # Create combats
    combats = [
        {"name": "Battle of Helm's Deep", "campaign_name": "Las dos torres"},
        {"name": "Battle of Pelennor Fields", "campaign_name": "Las dos torres"},
        {"name": "Duel on Mustafar", "campaign_name": "La amenaza fantasma"},
        {"name": "Battle of Endor", "campaign_name": "El ataque de los clones"},
        {"name": "Battle of Hoth", "campaign_name": "El ataque de los clones"},
        {"name": "Fight in the Temple of Doom", "campaign_name": "Raiders of the Lost Ark"},
        {"name": "Battle at the Canyon of the Crescent Moon", "campaign_name": "The Last Crusade"},
    ]

    for combat_data in combats:
        campaign = Campaign.get_by_name(combat_data["campaign_name"])
        Combat.create(combat_data["name"], campaign.id)
        print(f"Created combat: {combat_data['name']} for campaign: {combat_data['campaign_name']}")

if __name__ == "__main__":
    create_initial_users()
    create_initial_data()
