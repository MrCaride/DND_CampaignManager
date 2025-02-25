class Campaign:
    def __init__(self, id, name, master_id):
        self.id = id
        self.name = name
        self.master_id = master_id
        self.missions = []

    def add_mission(self, mission):
        self.missions.append(mission)

    def remove_mission(self, mission):
        self.missions.remove(mission)

    def get_missions(self):
        return self.missions

    def __repr__(self):
        return f"<Campaign {self.name} (ID: {self.id})>"