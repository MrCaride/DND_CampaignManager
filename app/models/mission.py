from app import db
from sirope import OID

class Mission:
    def __init__(self, name, description, campaign_name, rewards=None, votes=0, voters=None):
        self.name = name
        self.description = description
        self.campaign_name = campaign_name
        self.rewards = rewards
        self.votes = votes
        self.voters = voters or []
        self._id = None

    @property
    def id(self):
        return str(self._id) if self._id else None

    @classmethod
    def get_by_id(cls, mission_id):
        try:
            oid = OID.from_str(mission_id)
            mission = db.load(oid)
            if isinstance(mission, cls):
                return mission
        except:
            pass
        return None

    @classmethod
    def create(cls, name, description, campaign_name, rewards=None):
        mission = cls(name, description, campaign_name, rewards)
        oid = db.save(mission)
        mission._id = oid
        return mission

    @classmethod
    def get_all(cls):
        return list(db.load_all(cls))

    def vote(self, user):
        user_id = int(user.id)
        if user_id not in self.voters:
            self.voters.append(user_id)
            self.votes += 1
            db.save(self)

    def unvote(self, user):
        user_id = int(user.id)
        if user_id in self.voters:
            self.voters.remove(user_id)
            self.votes -= 1
            db.save(self)

    @classmethod
    def get_by_campaign(cls, campaign_name):
        return list(db.filter(cls, lambda m: m.campaign_name == campaign_name))