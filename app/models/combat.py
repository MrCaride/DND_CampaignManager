from app import db

class Combat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # ...otros campos necesarios...

    def __init__(self, id, mission_id):
        self.id = id
        self.mission_id = mission_id
        self.participants = []
        self.turn_order = []
        self.active = False

    def start_combat(self):
        self.active = True
        self.determine_turn_order()

    def end_combat(self):
        self.active = False
        self.participants.clear()
        self.turn_order.clear()

    def add_participant(self, character):
        self.participants.append(character)

    def determine_turn_order(self):
        # Logic to determine turn order based on initiative
        self.turn_order = sorted(self.participants, key=lambda x: x.initiative, reverse=True)

    def next_turn(self):
        if self.turn_order:
            current_turn = self.turn_order.pop(0)
            self.turn_order.append(current_turn)
            return current_turn
        return None

    def get_status(self):
        return {
            "active": self.active,
            "participants": [participant.name for participant in self.participants],
            "turn_order": [character.name for character in self.turn_order]
        }