from app import redis_client

class Mission:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def get_by_id(cls, mission_id):
        mission_data = redis_client.hgetall(f"mission:{mission_id}")
        if mission_data:
            mission = cls(mission_data[b'name'].decode('utf-8'), mission_data[b'description'].decode('utf-8'))
            mission.id = mission_id
            return mission
        return None

    @classmethod
    def create(cls, name, description):
        mission = cls(name, description)
        mission_id = redis_client.incr("mission_id")  # Increment mission ID
        mission.id = mission_id
        redis_client.hmset(f"mission:{mission_id}", {
            "name": name,
            "description": description
        })
        return mission

    @classmethod
    def get_all(cls):
        mission_ids = redis_client.keys("mission:*")
        missions = []
        for mission_id in mission_ids:
            mission = cls.get_by_id(mission_id.split(b':')[1])
            if mission:
                missions.append(mission)
        return missions