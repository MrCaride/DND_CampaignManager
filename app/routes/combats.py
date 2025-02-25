from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.combat import Combat
from app.models.mission import Mission
from app.models.campaign import Campaign
from app import redis_client, db

combats_bp = Blueprint('combats', __name__)

@combats_bp.route('/<int:campaign_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_combats(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to manage combats for this campaign.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign_id))

    if request.method == 'POST':
        name = request.form['name']
        new_combat = Combat(name=name, campaign_id=campaign_id)
        db.session.add(new_combat)
        db.session.commit()
        flash('Combat created successfully!', 'success')
        return redirect(url_for('combats.manage_combats', campaign_id=campaign_id))
    
    combats = Combat.query.filter_by(campaign_id=campaign_id).all()
    return render_template('combats/manage.html', campaign=campaign, combats=combats)

@combats_bp.route('/<int:campaign_id>/view', methods=['GET'])
@login_required
def view_combats(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    combats = Combat.query.filter_by(campaign_id=campaign_id).all()
    return render_template('combats/view.html', campaign=campaign, combats=combats)

@combats_bp.route('/')
@login_required
def list_combats():
    combats = Combat.query.filter_by(user_id=current_user.id).all()
    return render_template('combats/list.html', combats=combats)

@combats_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_combat():
    if request.method == 'POST':
        name = request.form['name']
        new_combat = Combat(name=name, user_id=current_user.id)
        db.session.add(new_combat)
        db.session.commit()
        flash('Combat created successfully!', 'success')
        return redirect(url_for('combats.list_combats'))
    return render_template('combats/new.html')

@combats_bp.route('/initiate/<int:mission_id>', methods=['GET', 'POST'])
@login_required
def initiate_combat(mission_id):
    mission = Mission.query.get(mission_id)
    if not mission:
        flash('Mission not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        # Logic to initiate combat
        combat = Combat(mission_id=mission.id)
        redis_client.set(f'combat:{combat.id}', combat)
        flash('Combat initiated successfully!', 'success')
        return redirect(url_for('combats.view_combat', combat_id=combat.id))

    return render_template('combats/initiate_combat.html', mission=mission)

@combats_bp.route('/view/<int:combat_id>', methods=['GET'])
@login_required
def view_combat(combat_id):
    combat_data = redis_client.get(f'combat:{combat_id}')
    if not combat_data:
        flash('Combat not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    return render_template('combats/view_combat.html', combat=combat_data)

@combats_bp.route('/end/<int:combat_id>', methods=['POST'])
@login_required
def end_combat(combat_id):
    combat_data = redis_client.get(f'combat:{combat_id}')
    if not combat_data:
        flash('Combat not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    # Logic to end combat
    redis_client.delete(f'combat:{combat_id}')
    flash('Combat ended successfully!', 'success')
    return redirect(url_for('campaigns.list_campaigns'))

@combats_bp.route('/')
def combats_index():
    return render_template('combats/index.html')