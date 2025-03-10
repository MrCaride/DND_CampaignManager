from app import redis_client

class Campaign:
    def __init__(self, name, is_public, master_id=None, allowed_players=None):
        self.name = name
        self.is_public = is_public
        self.master_id = master_id
        self.allowed_players = allowed_players if allowed_players else []

    @classmethod
    def get_by_id(cls, campaign_id):
        campaign_data = redis_client.hgetall(f"campaign:{campaign_id}")
        if campaign_data:
            allowed_players = campaign_data.get(b'allowed_players', b'').decode('utf-8').split(',')
            campaign = cls(
                campaign_data[b'name'].decode('utf-8'),
                bool(int(campaign_data[b'is_public'])),
                int(campaign_data.get(b'master_id', 0)),
                allowed_players
            )
            campaign.id = int(campaign_id)
            print(f"Fetched campaign by ID {campaign_id}: {campaign.name}, allowed players: {campaign.allowed_players}")  # Debug statement
            return campaign
        print(f"No campaign data found for ID {campaign_id}")  # Debug statement
        return None

    @classmethod
    def create(cls, name, is_public, master_id=None, allowed_players=None):
        # Check if a campaign with the same name already exists
        existing_campaign = cls.get_by_name(name)
        if existing_campaign:
            print(f"Campaign with name {name} already exists with ID {existing_campaign.id}")
            return existing_campaign

        campaign = cls(name, is_public, master_id, allowed_players)
        campaign_id = redis_client.incr("campaign_id")  # Increment campaign ID
        campaign.id = campaign_id
        campaign_data = {
            "name": name,
            "is_public": int(is_public),  # Convert boolean to integer
            "master_id": master_id if master_id is not None else '',
            "allowed_players": ','.join(allowed_players) if allowed_players else ''
        }
        redis_client.hmset(f"campaign:{campaign_id}", campaign_data)
        print(f"Created campaign: {campaign.name} with ID {campaign.id}, allowed players: {campaign.allowed_players}")  # Debug statement
        return campaign

    @classmethod
    def get_all(cls):
        campaign_ids = redis_client.keys("campaign:*")
        campaigns = []
        for campaign_id in campaign_ids:
            campaign = cls.get_by_id(int(campaign_id.split(b':')[1]))
            if campaign:
                campaigns.append(campaign)
        print(f"All campaigns fetched: {[campaign.name for campaign in campaigns]}")  # Debug statement
        return campaigns

    @classmethod
    def get_by_name(cls, name):
        campaign_ids = redis_client.keys("campaign:*")
        for campaign_id in campaign_ids:
            if redis_client.type(campaign_id) == b'hash':
                campaign_data = redis_client.hgetall(campaign_id)
                if campaign_data and campaign_data[b'name'].decode('utf-8') == name:
                    return cls.get_by_id(int(campaign_id.split(b':')[1]))
        return None