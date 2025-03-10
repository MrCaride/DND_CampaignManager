from app import redis_client

class Combat:
    def __init__(self, name, campaign_id):
        self.name = name
        self.campaign_id = campaign_id
        self.participants = []

    @classmethod
    def get_by_id(cls, combat_id):
        combat_data = redis_client.hgetall(f"combat:{combat_id}")
        if combat_data:
            combat = cls(
                combat_data[b'name'].decode('utf-8'),
                int(combat_data[b'campaign_id'])
            )
            combat.id = combat_id
            participants_data = redis_client.smembers(f"combat:{combat_id}:participants")
            combat.participants = [int(participant) for participant in participants_data]
            return combat
        return None

    @classmethod
    def create(cls, name, campaign_id):
        combat = cls(name, campaign_id)
        combat_id = redis_client.incr("combat_id")  # Increment combat ID
        combat.id = combat_id
        redis_client.hmset(f"combat:{combat_id}", {
            "name": name,
            "campaign_id": campaign_id
        })
        return combat

    @classmethod
    def get_all(cls):
        combat_ids = redis_client.keys("combat:*")
        combats = []
        for combat_id in combat_ids:
            combat = cls.get_by_id(int(combat_id.split(b':')[1]))
            if combat:
                combats.append(combat)
        return combats

    def add_participant(self, character):
        redis_client.sadd(f"combat:{self.id}:participants", character.id)
        self.participants.append(character.id)

    def remove_participant(self, character):
        redis_client.srem(f"combat:{self.id}:participants", character.id)
        self.participants.remove(character.id)