from app import db

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    def __init__(self, name, description, campaign_id):
        self.name = name
        self.description = description
        self.campaign_id = campaign_id

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