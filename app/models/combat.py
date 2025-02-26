from app import db

combat_participants = db.Table('combat_participants',
    db.Column('combat_id', db.Integer, db.ForeignKey('combat.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), primary_key=True)
)

class Combat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    participants = db.relationship('Character', secondary=combat_participants, backref='combats')
    active = db.Column(db.Boolean, default=False)
    participants_data = db.Column(db.JSON, nullable=True)  # Nuevo campo para guardar los datos de los participantes

    def __init__(self, name, campaign_id):
        self.name = name
        self.campaign_id = campaign_id

    def start_combat(self):
        self.active = True
        self.determine_turn_order()

    def end_combat(self):
        self.active = False
        self.participants.clear()
        self.turn_order.clear()

    def add_participant(self, character):
        participant_data = {
            'name': character.name,
            'totalHP': character.hit_points,
            'remainingHP': character.hit_points,
            'bonus': character.bonus
        }
        if self.participants_data is None:
            self.participants_data = []
        self.participants_data.append(participant_data)
        self.participants.append(character)
        db.session.commit()

    def remove_participant(self, character):
        if character in self.participants:
            self.participants.remove(character)
            db.session.commit()

    def determine_turn_order(self):
        # Logic to determine turn order based on initiative
        self.turn_order = sorted(self.participants, key=lambda x: x.initiative, reverse=True)


    def get_status(self):
        return {
            "active": self.active,
            "participants": [participant.name for participant in self.participants],
            "turn_order": [character.name for character in self.turn_order]
        }

    def save_state(self):
        state = {
            "active": self.active,
            "participants_data": self.participants_data,
            "turn_order": [character.id for character in self.turn_order]
        }
        return state

    def restore_state(self, state):
        self.active = state["active"]
        self.participants_data = state["participants_data"]
        self.turn_order = [Character.query.get(character_id) for character_id in state["turn_order"]]
        db.session.commit()