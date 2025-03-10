from app import redis_client

class Mission:
    def __init__(self, name, description, campaign_name, rewards=None, votes=0, voters=None):
        self.name = name
        self.description = description
        self.campaign_name = campaign_name
        self.rewards = rewards
        self.votes = votes
        self.voters = voters or []

    @classmethod
    def get_by_id(cls, mission_id):
        mission_data = redis_client.hgetall(f"mission:{mission_id}")
        if mission_data:
            try:
                voters = redis_client.smembers(f"mission:{mission_id}:votes")
                voters = [int(voter) for voter in voters]
                mission = cls(
                    mission_data[b'name'].decode('utf-8'),
                    mission_data[b'description'].decode('utf-8'),
                    mission_data.get(b'campaign_name', b'').decode('utf-8'),  # Handle missing campaign_name
                    mission_data.get(b'rewards', b'').decode('utf-8'),
                    int(mission_data.get(b'votes', b'0')),
                    voters
                )
            except KeyError as e:
                return None
            mission.id = mission_id
            return mission
        return None

    @classmethod
    def create(cls, name, description, campaign_name, rewards=None):
        mission = cls(name, description, campaign_name, rewards)
        mission_id = redis_client.incr("mission_id")  # Increment mission ID
        mission.id = mission_id
        redis_client.hmset(f"mission:{mission_id}", {
            "name": name,
            "description": description,
            "campaign_name": campaign_name,
            "rewards": rewards or '',
            "votes": mission.votes
        })
        return mission

    @classmethod
    def get_all(cls):
        mission_ids = redis_client.keys("mission:*")
        missions = []
        for mission_id in mission_ids:
            mission = cls.get_by_id(int(mission_id.split(b':')[1]))
            if mission:
                missions.append(mission)
        return missions

    def vote(self, user):
        redis_client.sadd(f"mission:{self.id}:votes", user.id)
        self.votes += 1
        self.voters.append(user.id)
        redis_client.hset(f"mission:{self.id}", "votes", self.votes)

    def unvote(self, user):
        redis_client.srem(f"mission:{self.id}:votes", user.id)
        self.votes -= 1
        self.voters.remove(user.id)
        redis_client.hset(f"mission:{self.id}", "votes", self.votes)