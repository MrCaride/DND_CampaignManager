from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.combat import Combat
from app.models.mission import Mission
from app import redis_client

combats_bp = Blueprint('combats', __name__)

@combats_bp.route('/combat/<int:mission_id>', methods=['GET', 'POST'])
@login_required
def initiate_combat(mission_id):
    mission = Mission.query.get(mission_id)
    if not mission:
        flash('Mission not found.', 'danger')
        return redirect(url_for('campaigns.view_campaigns'))

    if request.method == 'POST':
        # Logic to initiate combat
        combat = Combat(mission_id=mission.id)
        redis_client.set(f'combat:{combat.id}', combat)
        flash('Combat initiated successfully!', 'success')
        return redirect(url_for('combats.view_combat', combat_id=combat.id))

    return render_template('combats/initiate_combat.html', mission=mission)

@combats_bp.route('/combat/view/<int:combat_id>', methods=['GET'])
@login_required
def view_combat(combat_id):
    combat_data = redis_client.get(f'combat:{combat_id}')
    if not combat_data:
        flash('Combat not found.', 'danger')
        return redirect(url_for('campaigns.view_campaigns'))

    return render_template('combats/view_combat.html', combat=combat_data)

@combats_bp.route('/combat/end/<int:combat_id>', methods=['POST'])
@login_required
def end_combat(combat_id):
    combat_data = redis_client.get(f'combat:{combat_id}')
    if not combat_data:
        flash('Combat not found.', 'danger')
        return redirect(url_for('campaigns.view_campaigns'))

    # Logic to end combat
    redis_client.delete(f'combat:{combat_id}')
    flash('Combat ended successfully!', 'success')
    return redirect(url_for('campaigns.view_campaigns'))