from flask import current_app
from redis import Redis
from app import redis_client

class Character:
    def __init__(self, name, race, character_class, level):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.level = level

    @classmethod
    def get_by_id(cls, character_id):
        character_data = redis_client.hgetall(f"character:{character_id}")
        if character_data:
            character = cls(character_data[b'name'].decode('utf-8'), character_data[b'race'].decode('utf-8'), character_data[b'character_class'].decode('utf-8'), int(character_data[b'level']))
            character.id = character_id
            return character
        return None

    @classmethod
    def create(cls, name, race, character_class, level):
        character = cls(name, race, character_class, level)
        character_id = redis_client.incr("character_id")  # Increment character ID
        character.id = character_id
        redis_client.hmset(f"character:{character_id}", {
            "name": name,
            "race": race,
            "character_class": character_class,
            "level": level
        })
        return character

    @classmethod
    def get_all(cls):
        character_ids = redis_client.keys("character:*")
        characters = []
        for character_id in character_ids:
            character = cls.get_by_id(character_id.split(b':')[1])
            if character:
                characters.append(character)
        return characters