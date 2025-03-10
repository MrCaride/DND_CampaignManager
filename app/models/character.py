from flask import current_app
from redis import Redis
from app import redis_client

class Character:
    def __init__(self, name, race, character_class, level, user_id=None, user_username=None, campaign_id=None, strength=None, dexterity=None, constitution=None, intelligence=None, wisdom=None, charisma=None, armor_class=None, initiative=None, hit_points=None, speed=None):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.level = level
        self.user_id = user_id
        self.user_username = user_username
        self.campaign_id = campaign_id  # Añadimos el atributo campaign_id
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.armor_class = armor_class
        self.initiative = initiative
        self.hit_points = hit_points
        self.speed = speed

    @classmethod
    def get_by_id(cls, character_id):
        character_data = redis_client.hgetall(f"character:{character_id}")
        print(f"Fetched data for character ID {character_id}: {character_data}")  # Debug statement
        if character_data:
            try:
                character = cls(
                    character_data[b'name'].decode('utf-8'),
                    character_data[b'race'].decode('utf-8'),
                    character_data[b'character_class'].decode('utf-8'),
                    int(character_data[b'level']),
                    int(character_data[b'user_id']),
                    character_data.get(b'user_username', b'').decode('utf-8'),  # Handle missing user_username
                    int(character_data.get(b'campaign_id', 0)),  # Añadimos el atributo campaign_id
                    int(character_data.get(b'strength', 0)),
                    int(character_data.get(b'dexterity', 0)),
                    int(character_data.get(b'constitution', 0)),
                    int(character_data.get(b'intelligence', 0)),
                    int(character_data.get(b'wisdom', 0)),
                    int(character_data.get(b'charisma', 0)),
                    int(character_data.get(b'armor_class', 0)),
                    int(character_data.get(b'initiative', 0)),
                    int(character_data.get(b'hit_points', 0)),
                    int(character_data.get(b'speed', 0))
                )
                character.id = int(character_id)
                return character
            except Exception as e:
                print(f"Error decoding character data for ID {character_id}: {e}")  # Debug statement
        return None

    @classmethod
    def create(cls, name, race, character_class, level, user_id, user_username, campaign_id=None, strength=None, dexterity=None, constitution=None, intelligence=None, wisdom=None, charisma=None, armor_class=None, initiative=None, hit_points=None, speed=None):
        character = cls(name, race, character_class, level, user_id, user_username, campaign_id, strength, dexterity, constitution, intelligence, wisdom, charisma, armor_class, initiative, hit_points, speed)
        character_id = redis_client.incr("character_id")  # Increment character ID
        character.id = character_id
        character_data = {
            "name": name,
            "race": race,
            "character_class": character_class,
            "level": level,
            "user_id": user_id,
            "user_username": user_username,
            "campaign_id": campaign_id if campaign_id is not None else 0,  # Añadimos el atributo campaign_id
            "strength": strength if strength is not None else 0,
            "dexterity": dexterity if dexterity is not None else 0,
            "constitution": constitution if constitution is not None else 0,
            "intelligence": intelligence if intelligence is not None else 0,
            "wisdom": wisdom if wisdom is not None else 0,
            "charisma": charisma if charisma is not None else 0,
            "armor_class": armor_class if armor_class is not None else 0,
            "initiative": initiative if initiative is not None else 0,
            "hit_points": hit_points if hit_points is not None else 0,
            "speed": speed if speed is not None else 0
        }
        redis_client.hmset(f"character:{character_id}", character_data)
        print(f"Created character: {character.name} with ID {character.id} for user ID {user_id} and username {user_username}")
        print(f"Character data saved: {character_data}")  # Debug statement
        # Verify that the data was saved correctly
        saved_data = redis_client.hgetall(f"character:{character_id}")
        print(f"Saved data for character ID {character_id}: {saved_data}")  # Debug statement
        return character

    @classmethod
    def get_all(cls):
        character_ids = redis_client.keys("character:*")
        print(f"Character IDs fetched: {character_ids}")  # Debug statement
        characters = []
        for character_id in character_ids:
            character = cls.get_by_id(character_id.split(b':')[1].decode('utf-8'))  # Decode character_id
            if character:
                characters.append(character)
        print(f"All characters fetched: {[(char.name, char.user_username) for char in characters]}")  # Debug statement
        return characters

    @classmethod
    def get_by_username(cls, user_username):
        characters = cls.get_all()
        print(f"Characters fetched for user_username {user_username}: {[(char.name, char.user_username) for char in characters]}")  # Debug statement
        user_characters = [character for character in characters if character.user_username == user_username]
        print(f"Fetched characters for user_username {user_username}: {[(char.name, char.user_username) for char in user_characters]}")  # Debug statement
        return user_characters

    @classmethod
    def get_by_user_and_campaign(cls, user_id, campaign_id):
        character_ids = redis_client.keys("character:*")
        for character_id in character_ids:
            character = cls.get_by_id(int(character_id.split(b':')[1]))
            if character and character.user_id == user_id and character.campaign_id == campaign_id:
                return character
        return None