from app import db
from sirope import OID

class Character:
    def __init__(self, name, race, character_class, level, user_id=None, user_username=None, campaign_id=None, 
                 strength=None, dexterity=None, constitution=None, intelligence=None, wisdom=None, 
                 charisma=None, armor_class=None, initiative=None, hit_points=None, speed=None, campaign=None):
        self.name = name
        self.race = race
        self.character_class = character_class
        self.level = int(level) if level else 1
        self.user_id = user_id
        self.user_username = user_username
        self.campaign_id = campaign_id
        self.strength = int(strength) if strength else 10
        self.dexterity = int(dexterity) if dexterity else 10
        self.constitution = int(constitution) if constitution else 10
        self.intelligence = int(intelligence) if intelligence else 10
        self.wisdom = int(wisdom) if wisdom else 10
        self.charisma = int(charisma) if charisma else 10
        self.armor_class = int(armor_class) if armor_class else 10
        self.initiative = int(initiative) if initiative else 0
        self.hit_points = int(hit_points) if hit_points else 10
        self.speed = int(speed) if speed else 30
        self.campaign = campaign
        self._id = None

    def __getstate__(self):
        """Método especial para pickle/Sirope - asegura que el _id se guarde"""
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """Método especial para pickle/Sirope - asegura que el _id se restaure"""
        self.__dict__.update(state)

    @property
    def id(self):
        """Retorna el ID en formato string"""
        return str(self._id) if self._id else None

    @classmethod
    def get_by_id(cls, character_id):
        try:
            if not character_id:
                return None

            # Si el ID tiene formato 'app.models.character.Character@0', extraer el número
            if '@' in str(character_id):
                oid_num = int(str(character_id).split('@')[-1])
                all_characters = list(db.load_all(cls))
                # Buscar el personaje con el _id correspondiente
                for character in all_characters:
                    if hasattr(character, '_id') and character._id and str(character._id).endswith(f'@{oid_num}'):
                        return character
        except Exception as e:
            print(f"Error loading character by ID: {str(e)}")
        return None

    @classmethod
    def create(cls, name, race, character_class, level, user_id, user_username, campaign_id=None, 
              strength=None, dexterity=None, constitution=None, intelligence=None, wisdom=None, 
              charisma=None, armor_class=None, initiative=None, hit_points=None, speed=None, campaign=None):
        character = cls(name, race, character_class, level, user_id, user_username, campaign_id,
                      strength, dexterity, constitution, intelligence, wisdom, charisma,
                      armor_class, initiative, hit_points, speed, campaign)
        oid = db.save(character)
        character._id = oid
        
        # Volver a guardar para asegurar que el _id se persiste
        db.save(character)
        return character

    @classmethod
    def get_all(cls):
        characters = list(db.load_all(cls))
        # Asegurar que todos los personajes tienen su ID
        updated_characters = []
        for character in characters:
            if not hasattr(character, '_id') or not character._id:
                oid = db.save(character)
                character._id = oid
                db.save(character)
            updated_characters.append(character)
        return updated_characters

    @classmethod
    def get_by_username(cls, user_username):
        characters = list(db.filter(cls, lambda char: char.user_username == user_username))
        # Asegurar que todos los personajes tienen su ID
        updated_characters = []
        for character in characters:
            if not hasattr(character, '_id') or not character._id:
                oid = db.save(character)
                character._id = oid
                db.save(character)
            updated_characters.append(character)
        return updated_characters

    @classmethod
    def get_by_user_and_campaign(cls, user_id, campaign_name):
        # Convertir user_id a string para comparación consistente
        user_id = str(user_id)
        return db.find_first(cls, lambda char: str(char.user_id) == user_id and char.campaign == campaign_name)