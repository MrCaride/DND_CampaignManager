from app import db
from sirope import OID

class Mission:
    def __init__(self, name, description, campaign_name=None, rewards=0):
        self.name = name
        self.description = description
        self.campaign_name = campaign_name
        self.rewards = int(rewards) if rewards else 0
        self._id = None
        self.votes = 0
        self.voters = []

    def __getstate__(self):
        """Método especial para pickle/Sirope - asegura que el _id se guarde"""
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """Método especial para pickle/Sirope - asegura que el _id se restaure"""
        self.__dict__.update(state)

    @property
    def id(self):
        """Retorna el ID numérico extraído del OID de Sirope"""
        if self._id and '@' in str(self._id):
            return int(str(self._id).split('@')[-1])
        return None

    @property
    def full_id(self):
        """Retorna el ID completo de Sirope"""
        return str(self._id) if self._id else None

    @classmethod
    def get_by_id(cls, mission_id):
        if not mission_id:
            return None
        try:
            all_missions = list(db.load_all(cls))

            # Convert mission_id to string for comparison
            mission_id_str = str(mission_id)
            
            # First try direct ID match
            for mission in all_missions:
                if hasattr(mission, '_id') and mission._id and str(mission._id) == mission_id_str:
                    return mission

            # Then try numeric ID match
            if mission_id_str.isdigit():
                for mission in all_missions:
                    if hasattr(mission, '_id') and mission._id and str(mission._id).endswith(f"@{mission_id_str}"):
                        return mission
                        
            # Finally try OID format match
            if '@' in mission_id_str:
                oid_num = mission_id_str.split('@')[-1]
                for mission in all_missions:
                    if hasattr(mission, '_id') and mission._id and str(mission._id).endswith(f"@{oid_num}"):
                        return mission

            return None
        except Exception as e:
            return None
            
    @classmethod
    def create(cls, name, description, campaign_name=None, rewards=0):
        mission = cls(name, description, campaign_name, rewards)
        oid = db.save(mission)
        mission._id = oid
        
        # Volver a guardar para asegurar que el _id se persiste
        db.save(mission)
        return mission

    @classmethod
    def get_all(cls):
        missions = list(db.load_all(cls))
        # Asegurar que todas las misiones tienen su ID
        updated_missions = []
        for mission in missions:
            if not hasattr(mission, '_id') or not mission._id:
                oid = db.save(mission)
                mission._id = oid
                db.save(mission)
            updated_missions.append(mission)
        return updated_missions

    @classmethod
    def get_by_campaign(cls, campaign_name):
        if not campaign_name:
            return []
        missions = list(db.filter(cls, lambda m: m.campaign_name == campaign_name))
        # Asegurar que todas las misiones tienen su ID
        updated_missions = []
        for mission in missions:
            if not hasattr(mission, '_id') or not mission._id:
                oid = db.save(mission)
                mission._id = oid
                db.save(mission)
            updated_missions.append(mission)
        return updated_missions

    def vote(self, user):
        """Add a vote from a user for this mission"""
        if user.username not in self.voters:
            self.votes += 1
            self.voters.append(user.username)
            db.save(self)
            return True
        return False

    def unvote(self, user):
        """Remove a vote from a user for this mission"""
        if user.username in self.voters:
            self.votes -= 1
            self.voters.remove(user.username)
            db.save(self)
            return True
        return False