from flask import current_app
from redis import Redis
from app import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    character_class = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    strength = db.Column(db.Integer, nullable=False, default=10)
    dexterity = db.Column(db.Integer, nullable=False, default=10)
    constitution = db.Column(db.Integer, nullable=False, default=10)
    intelligence = db.Column(db.Integer, nullable=False, default=10)
    wisdom = db.Column(db.Integer, nullable=False, default=10)
    charisma = db.Column(db.Integer, nullable=False, default=10)
    hit_points = db.Column(db.Integer, nullable=False, default=10)
    armor_class = db.Column(db.Integer, nullable=False, default=10)
    initiative = db.Column(db.Integer, nullable=False, default=0)
    speed = db.Column(db.Integer, nullable=False, default=30)
    # ...otros campos necesarios...

    def __init__(self, name, user_id, race, character_class):
        self.name = name
        self.user_id = user_id
        self.race = race
        self.character_class = character_class
        # ...inicializar otros campos necesarios...

    def save(self):
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        redis.hset(f'character:{self.id}', mapping={
            'name': self.name,
            'user_id': self.user_id,
            'race': self.race,
            'character_class': self.character_class,
            'level': self.level,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'constitution': self.constitution,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'charisma': self.charisma,
            'hit_points': self.hit_points,
            'armor_class': self.armor_class,
            'initiative': self.initiative,
            'speed': self.speed
        })

    @classmethod
    def get(cls, id):
        redis = Redis.from_url(current_app.config['REDIS_URL'])
        data = redis.hgetall(f'character:{id}')
        if data:
            return cls(
                id=id,
                name=data.get(b'name').decode('utf-8'),
                user_id=data.get(b'user_id').decode('utf-8'),
                race=data.get(b'race').decode('utf-8'),
                character_class=data.get(b'character_class').decode('utf-8'),
                level=int(data.get(b'level')),
                strength=int(data.get(b'strength')),
                dexterity=int(data.get(b'dexterity')),
                constitution=int(data.get(b'constitution')),
                intelligence=int(data.get(b'intelligence')),
                wisdom=int(data.get(b'wisdom')),
                charisma=int(data.get(b'charisma')),
                hit_points=int(data.get(b'hit_points')),
                armor_class=int(data.get(b'armor_class')),
                initiative=int(data.get(b'initiative')),
                speed=int(data.get(b'speed'))
            )
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