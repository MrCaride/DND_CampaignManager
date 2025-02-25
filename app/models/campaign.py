from app import db

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    allowed_players = db.Column(db.PickleType, default=[])

    def add_mission(self, mission):
        self.missions.append(mission)

    def remove_mission(self, mission):
        self.missions.remove(mission)

    def get_missions(self):
        return self.missions

    def add_player(self, player_id):
        if player_id not in self.allowed_players:
            self.allowed_players.append(player_id)
            db.session.commit()

    def remove_player(self, player_id):
        if player_id in self.allowed_players:
            self.allowed_players.remove(player_id)
            db.session.commit()

    def __repr__(self):
        return f"<Campaign {self.name} (ID: {self.id})>"