from flask import current_app
from redis import Redis
from app import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('characters', lazy=True))  # Añade la relación con User
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
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)  # Nueva propiedad
    bonus = db.Column(db.String(50), nullable=True)

    def __init__(self, name, race, character_class, user_id, level=1, strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10, hit_points=10, armor_class=10, initiative=0, speed=30, bonus=None):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.user_id = user_id
        self.level = level
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.hit_points = hit_points
        self.armor_class = armor_class
        self.initiative = initiative
        self.speed = speed
        self.bonus = bonus
        

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
            'speed': self.speed,
            'campaign_id': self.campaign_id,
            'bonus': self.bonus
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
                speed=int(data.get(b'speed')),
                campaign_id=int(data.get(b'campaign_id')) if data.get(b'campaign_id') else None,
                bonus=data.get(b'bonus').decode('utf-8') if data.get(b'bonus') else None
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