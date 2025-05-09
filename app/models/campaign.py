from app import db
from sirope import OID

class Campaign:
    def __init__(self, name, is_public, master_id=None, allowed_players=None):
        self.name = name
        self.is_public = is_public
        self.master_id = master_id
        self.allowed_players = allowed_players if allowed_players else []
        self._id = None

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @property
    def id(self):
        """Retorna el ID como string"""
        return str(self._id) if self._id else None

    @classmethod
    def get_by_id(cls, campaign_id):
        if campaign_id is None:
            return None
            
        try:
            print(f"Searching for campaign with ID: {campaign_id}")
            all_campaigns = list(db.load_all(cls))
            print(f"Found {len(all_campaigns)} total campaigns")
            
            # Si el ID es numérico, buscamos la campaña correspondiente
            if isinstance(campaign_id, (int, str)):
                campaign_id_str = str(campaign_id)
                
                # Intentar encontrar por el ID numérico al final del OID
                for campaign in all_campaigns:
                    if hasattr(campaign, '_id') and campaign._id:
                        campaign_oid = str(campaign._id)
                        if campaign_oid.endswith(f"@{campaign_id_str}"):
                            print(f"Found campaign by numeric ID: {campaign.name}")
                            return campaign
                            
                # Intentar encontrar por el OID completo
                for campaign in all_campaigns:
                    if hasattr(campaign, '_id') and campaign._id and str(campaign._id) == campaign_id_str:
                        print(f"Found campaign by full OID: {campaign.name}")
                        return campaign
                        
            print(f"No campaign found with ID: {campaign_id}")
            return None
            
        except Exception as e:
            print(f"Error in get_by_id: {str(e)}")
            return None

    @classmethod
    def create(cls, name, is_public, master_id=None, allowed_players=None):
        campaign = cls(name, is_public, master_id, allowed_players)
        oid = db.save(campaign)
        campaign._id = oid
        print(f"Created campaign: {campaign.name} with ID: {campaign._id}")
        db.save(campaign)
        return campaign

    @classmethod
    def get_all(cls):
        campaigns = list(db.load_all(cls))
        updated_campaigns = []
        for campaign in campaigns:
            if not hasattr(campaign, '_id') or not campaign._id:
                oid = db.save(campaign)
                campaign._id = oid
                db.save(campaign)
            updated_campaigns.append(campaign)
        return updated_campaigns

    @classmethod
    def get_by_name(cls, name):
        if not name:
            return None
        try:
            campaign = db.find_first(cls, lambda c: c.name == name)
            if campaign and (not hasattr(campaign, '_id') or not campaign._id):
                oid = db.save(campaign)
                campaign._id = oid
                db.save(campaign)
            return campaign
        except Exception as e:
            print(f"Error getting campaign by name: {str(e)}")
            return None