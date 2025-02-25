from app import db

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # autoincrement=True para que el id sea generado automáticamente
    name = db.Column(db.String(150), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # ...otros campos necesarios...

    def __init__(self, name, master_id):
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