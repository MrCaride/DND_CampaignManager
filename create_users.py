from app import create_app, db
from app.models.user import User
from app.models.character import Character
from app.models.campaign import Campaign
from app.models.mission import Mission
from sirope import OID
import random

app = create_app()

def clean_database():
    """Limpia la base de datos antes de crear nuevos datos"""
    db._redis.flushdb()
    print("Database cleaned")

def create_initial_users():
    users = [
        {"username": "master", "password": "masterpass", "role": "master"},
        {"username": "player1", "password": "playerpass1", "role": "player"},
        {"username": "player2", "password": "playerpass2", "role": "player"},
    ]

    created_users = []
    for user_data in users:
        if not User.get_by_username(user_data["username"]):
            user = User.create(user_data["username"], user_data["password"], user_data["role"])
            created_users.append(user)
            print(f"Created user: {user.username}")
        else:
            print(f"User {user_data['username']} already exists")
    return created_users

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

    created_users = {}
    for user_data in users:
        if not User.get_by_username(user_data["username"]):
            user = User.create(user_data["username"], user_data["password"], user_data["role"])
            created_users[user.username] = user

    # Create generic campaigns
    campaigns_data = [
        {"name": "La comunidad del anillo", "master_username": "master", "is_public": True},
        {"name": "Las dos torres", "master_username": "master", "is_public": False, "allowed_players": ["user1", "user2"]},
        {"name": "El retorno del rey", "master_username": "master", "is_public": True},
        {"name": "La amenaza fantasma", "master_username": "master", "is_public": False, "allowed_players": ["user3", "user4"]},
        {"name": "El ataque de los clones", "master_username": "master", "is_public": True},
        {"name": "Raiders of the Lost Ark", "master_username": "master2", "is_public": True},
        {"name": "The Last Crusade", "master_username": "master3", "is_public": False, "allowed_players": ["user1", "user3"]},
    ]

    created_campaigns = {}
    for campaign_data in campaigns_data:
        name = campaign_data["name"]
        existing = Campaign.get_by_name(name)
        if not existing:
            master = User.get_by_username(campaign_data["master_username"])
            if master:
                campaign = Campaign.create(
                    name=name,
                    is_public=campaign_data["is_public"],
                    master_id=master.id,
                    allowed_players=campaign_data.get("allowed_players", [])
                )
                created_campaigns[name] = campaign
        else:
            created_campaigns[name] = existing

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
        if user:
            character = Character.create(
                name=character_data["name"],
                race=character_data["race"],
                character_class=character_data["character_class"],
                level=character_data["level"],
                user_id=user.id,
                user_username=user.username
            )
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
        {"name": "Journey to Rivendell", "description": "Travel to Rivendell to seek counsel.", "campaign_name": "La comunidad del anillo"},
        {"name": "Ambush at Amon Hen", "description": "Defend against the ambush at Amon Hen.", "campaign_name": "La comunidad del anillo"},
        {"name": "Escape from Moria", "description": "Escape the mines of Moria.", "campaign_name": "La comunidad del anillo"},
    ]

    for mission_data in missions:
        campaign = created_campaigns.get(mission_data["campaign_name"])
        if campaign:
            rewards = random.randint(50, 500)
            mission = Mission.create(
                name=mission_data["name"],
                description=mission_data["description"],
                campaign_name=mission_data["campaign_name"],
                rewards=rewards
            )
            print(f"Created mission: {mission_data['name']} with rewards: {rewards}")

if __name__ == "__main__":
    clean_database()
    create_initial_users()
    create_initial_data()
