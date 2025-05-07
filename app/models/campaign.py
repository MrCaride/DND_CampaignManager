from app import db
from sirope import OID

class Campaign:
    def __init__(self, name, is_public, master_id=None, allowed_players=None):
        self.name = name
        self.is_public = is_public
        self.master_id = master_id
        self.allowed_players = allowed_players if allowed_players else []
        self._id = None

    @property
    def id(self):
        return str(self._id) if self._id else None

    @classmethod
    def get_by_id(cls, campaign_id):
        try:
            oid = OID.from_str(campaign_id)
            campaign = db.load(oid)
            if isinstance(campaign, cls):
                return campaign
        except:
            pass
        return None

    @classmethod
    def create(cls, name, is_public, master_id=None, allowed_players=None):
        # Check if campaign already exists using find_first
        existing = db.find_first(cls, lambda c: c.name == name)
        if existing:
            print(f"Campaign with name {name} already exists")
            return existing

        # Create new campaign
        campaign = cls(name, is_public, master_id, allowed_players)
        oid = db.save(campaign)
        campaign._id = oid
        print(f"Created new campaign: {campaign.name}")
        return campaign

    @classmethod
    def get_all(cls):
        return list(db.load_all(cls))

    @classmethod
    def get_by_name(cls, name):
        # Use find_first to get campaign by name
        return db.find_first(cls, lambda c: c.name == name)