from flask import current_app
from redis import Redis

class Character:
    def __init__(self, id, name, player_id):
        self.id = id
        self.name = name
        self.player_id = player_id

    def save(self):
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        redis.hset(f'character:{self.id}', mapping={
            'name': self.name,
            'player_id': self.player_id
        })

    @classmethod
    def get(cls, id):
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        data = redis.hgetall(f'character:{id}')
        if data:
            return cls(id=id, name=data.get(b'name').decode('utf-8'), player_id=data.get(b'player_id').decode('utf-8'))
        return None

    @classmethod
    def all(cls):
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        keys = redis.keys('character:*')
        characters = []
        for key in keys:
            character = cls.get(key.decode('utf-8').split(':')[1])
            if character:
                characters.append(character)
        return characters

    def delete(self):
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        redis.delete(f'character:{self.id}')