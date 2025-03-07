from app import redis_client

class Combat:
    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_id(cls, combat_id):
        combat_data = redis_client.hgetall(f"combat:{combat_id}")
        if combat_data:
            combat = cls(combat_data[b'name'].decode('utf-8'))
            combat.id = combat_id
            return combat
        return None

    @classmethod
    def create(cls, name):
        combat = cls(name)
        combat_id = redis_client.incr("combat_id")  # Increment combat ID
        combat.id = combat_id
        redis_client.hmset(f"combat:{combat_id}", {
            "name": name
        })
        return combat

    @classmethod
    def get_all(cls):
        combat_ids = redis_client.keys("combat:*")
        combats = []
        for combat_id in combat_ids:
            combat = cls.get_by_id(combat_id.split(b':')[1])
            if combat:
                combats.append(combat)
        return combats