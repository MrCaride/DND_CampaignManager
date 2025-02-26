from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.combat import Combat
from app.models.campaign import Campaign
from app.models.character import Character
from app import db

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

@combats_bp.route('/<int:combat_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    campaign = Campaign.query.get_or_404(combat.campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to edit this combat.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    if request.method == 'POST':
        combat.name = request.form['name']
        combat.active = request.form['active'] == 'true'
        db.session.commit()
        flash('Combat updated successfully!', 'success')
        return redirect(url_for('combats.manage_combats', campaign_id=campaign.id))
    
    return render_template('combats/edit.html', combat=combat)

@combats_bp.route('/<int:combat_id>/delete', methods=['POST'])
@login_required
def delete_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    campaign = Campaign.query.get_or_404(combat.campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to delete this combat.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    db.session.delete(combat)
    db.session.commit()
    flash('Combat deleted successfully!', 'success')
    return redirect(url_for('combats.manage_combats', campaign_id=campaign.id))

@combats_bp.route('/<int:combat_id>/join', methods=['POST'])
@login_required
def join_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    campaign = Campaign.query.get_or_404(combat.campaign_id)
    character = Character.query.filter_by(user_id=current_user.id, campaign_id=campaign.id).first()
    if character:
        combat.add_participant(character)
        db.session.commit()
        flash('Joined combat successfully!', 'success')
    else:
        flash('Failed to join combat.', 'danger')
    return redirect(url_for('combats.view_combats', campaign_id=campaign.id))

@combats_bp.route('/<int:combat_id>/leave', methods=['POST'])
@login_required
def leave_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    campaign = Campaign.query.get_or_404(combat.campaign_id)
    character = Character.query.filter_by(user_id=current_user.id, campaign_id=campaign.id).first()
    if character:
        combat.remove_participant(character)
        db.session.commit()
        flash('Left combat successfully!', 'success')
    return redirect(url_for('combats.view_combats', campaign_id=campaign.id))

@combats_bp.route('/view/<int:combat_id>', methods=['GET'])
@login_required
def view_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    return render_template('combats/view.html', combat=combat)

@combats_bp.route('/<int:campaign_id>/view_combats', methods=['GET'])
@login_required
def view_combats(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    combats = Combat.query.filter_by(campaign_id=campaign_id).all()
    return render_template('combats/view_combats.html', campaign=campaign, combats=combats)

@combats_bp.route('/<int:combat_id>/fight', methods=['GET', 'POST'])
@login_required
def fight_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    campaign = Campaign.query.get_or_404(combat.campaign_id)
    if request.method == 'POST':
        participants_data = request.json.get('participants', [])
        combat.participants_data = participants_data
        db.session.commit()
        return jsonify({"message": "Participants saved successfully"})
    
    # Verificar que participants_data no sea None
    if combat.participants_data is None:
        combat.participants_data = []

    return render_template('combats/fight.html', combat=combat, campaign=campaign)

@combats_bp.route('/<int:combat_id>/save_participants', methods=['POST'])
@login_required
def save_participants(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    participants_data = request.json.get('participants', [])
    combat.participants_data = participants_data
    db.session.commit()
    return jsonify({"message": "Participants saved successfully"})

@combats_bp.route('/end/<int:combat_id>', methods=['POST'])
@login_required
def end_combat(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    combat.end_combat()
    db.session.commit()
    flash('Combat ended successfully!', 'success')
    return redirect(url_for('campaigns.list_campaigns'))

@combats_bp.route('/get_participants/<int:combat_id>', methods=['GET'])
def get_participants(combat_id):
    combat = Combat.query.get_or_404(combat_id)
    participants_data = [
        {
            'name': participant.name,
            'totalHP': participant.hit_points,
            'bonus': participant.bonus
        }
        for participant in combat.participants
    ]
    return jsonify({'participants': participants_data})

@combats_bp.route('/delete_state/<int:combat_id>', methods=['POST'])
def delete_state(combat_id):
    combat = Combat.query.get(combat_id)
    if combat:
        initial_participants = [
            {
                'name': participant.name,
                'remainingHP': participant.hit_points,
                'totalHP': participant.hit_points
            }
            for participant in combat.participants
        ]
        combat.participants_data = initial_participants
        db.session.commit()
        return jsonify({'success': True, 'message': 'Combat state reset to initial participants successfully.'})
    return jsonify({'success': False, 'message': 'Combat not found.'})

@combats_bp.route('/')
def combats_index():
    return render_template('combats/index.html')