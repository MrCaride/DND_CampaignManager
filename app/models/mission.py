from app import db

# Define la tabla de asociación para los votos de las misiones
mission_votes = db.Table('mission_votes',
    db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    rewards = db.Column(db.String(500), nullable=True)  # Nuevo atributo
    votes = db.Column(db.Integer, default=0)  # Nuevo atributo
    voters = db.relationship('User', secondary=mission_votes, backref='voted_missions')  # Relación con User

    def __init__(self, name, description, campaign_id, rewards=None):
        self.name = name
        self.description = description
        self.campaign_id = campaign_id
        self.rewards = rewards

    def __repr__(self):
        return f"<Mission {self.name} (ID: {self.id})>"

    def create_mission(self):
        # Logic to create a new mission in the database
        pass

    def update_mission(self):
        # Logic to update an existing mission
        pass

    def delete_mission(self):
        # Logic to delete a mission
        pass

    def get_mission_details(self):
        # Logic to retrieve mission details
        pass

    def assign_objectives(self, objectives):
        self.objectives = objectives

    def complete_mission(self):
        # Logic to mark the mission as completed
        pass

    def vote(self, user):
        if user not in self.voters:
            self.voters.append(user)
            self.votes += 1
            db.session.commit()

    def unvote(self, user):
        if user in self.voters:
            self.voters.remove(user)
            self.votes -= 1
            db.session.commit()