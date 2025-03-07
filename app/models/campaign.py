from app import redis_client

class Campaign:
    def __init__(self, name, is_public):
        self.name = name
        self.is_public = is_public

    @classmethod
    def get_by_id(cls, campaign_id):
        campaign_data = redis_client.hgetall(f"campaign:{campaign_id}")
        if campaign_data:
            campaign = cls(campaign_data[b'name'].decode('utf-8'), bool(int(campaign_data[b'is_public'])))
            campaign.id = campaign_id
            return campaign
        return None

    @classmethod
    def create(cls, name, is_public):
        campaign = cls(name, is_public)
        campaign_id = redis_client.incr("campaign_id")  # Increment campaign ID
        campaign.id = campaign_id
        redis_client.hmset(f"campaign:{campaign_id}", {
            "name": name,
            "is_public": int(is_public)  # Convert boolean to integer
        })
        return campaign

    @classmethod
    def get_all(cls):
        campaign_ids = redis_client.keys("campaign:*")
        campaigns = []
        for campaign_id in campaign_ids:
            campaign = cls.get_by_id(campaign_id.split(b':')[1])
            if campaign:
                campaigns.append(campaign)
        return campaigns

    @classmethod
    def get_by_name(cls, name):
        campaign_ids = redis_client.keys("campaign:*")
        for campaign_id in campaign_ids:
            campaign_data = redis_client.hgetall(campaign_id)
            if campaign_data and campaign_data[b'name'].decode('utf-8') == name:
                return cls.get_by_id(campaign_id.split(b':')[1])
        return None