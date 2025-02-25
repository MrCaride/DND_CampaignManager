from app import db

allowed_players = db.Table('allowed_players',
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    allowed_players = db.relationship('User', secondary=allowed_players, lazy='subquery',
                                      backref=db.backref('campaigns', lazy=True))

    def add_mission(self, mission):
        self.missions.append(mission)

    def remove_mission(self, mission):
        self.missions.remove(mission)

    def get_missions(self):
        return self.missions

    def add_player(self, player):
        if player not in self.allowed_players:
            self.allowed_players.append(player)
            db.session.commit()

    def remove_player(self, player):
        if player in self.allowed_players:
            self.allowed_players.remove(player)
            db.session.commit()

    def __repr__(self):
        return f"<Campaign {self.name} (ID: {self.id})>"