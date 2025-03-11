from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.combat import Combat
from app.models.campaign import Campaign
from app.models.character import Character
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

combats_bp = Blueprint('combats', __name__)

@combats_bp.route('/<int:campaign_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_combats(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to manage combats for this campaign.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign_id))

    if request.method == 'POST':
        name = request.form['name']
        new_combat = Combat.create(name, campaign_id)
        flash('Combat created successfully!', 'success')
        return redirect(url_for('combats.manage_combats', campaign_id=campaign_id))
    
    # Filter combats by campaign_id
    combat_ids = redis_client.keys("combat:*")
    combats = []
    combat_ids_seen = set()
    for combat_id in combat_ids:
        combat = Combat.get_by_id(int(combat_id.split(b':')[1]))
        if combat and combat.campaign_id == campaign_id and combat.id not in combat_ids_seen:
            combats.append(combat)
            combat_ids_seen.add(combat.id)
    
    return render_template('combats/manage.html', campaign=campaign, combats=combats)

@combats_bp.route('/<int:combat_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_combat(combat_id):
    combat = Combat.get_by_id(combat_id)
    campaign = Campaign.get_by_id(combat.campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to edit this combat.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    if request.method == 'POST':
        combat.name = request.form['name']
        redis_client.hmset(f"combat:{combat_id}", {
            "name": combat.name
        })
        flash('Combat updated successfully!', 'success')
        return redirect(url_for('combats.manage_combats', campaign_id=campaign.id))
    
    return render_template('combats/edit.html', combat=combat)

@combats_bp.route('/<int:combat_id>/delete', methods=['POST'])
@login_required
def delete_combat(combat_id):
    combat = Combat.get_by_id(combat_id)
    campaign = Campaign.get_by_id(combat.campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to delete this combat.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    redis_client.delete(f"combat:{combat_id}")
    flash('Combat deleted successfully!', 'success')
    return redirect(url_for('combats.manage_combats', campaign_id=campaign.id))

@combats_bp.route('/<int:combat_id>/join', methods=['POST'])
@login_required
def join_combat(combat_id):
    combat = Combat.get_by_id(combat_id)
    campaign = Campaign.get_by_id(combat.campaign_id)
    character = Character.get_by_user_and_campaign(current_user.id, campaign.name)
    if character:
        if character.id not in combat.participants:
            combat.add_participant(character)
            redis_client.sadd(f"combat:{combat_id}:participants", character.id)
            print(f"Character {character.name} joined combat {combat.name}")  # Debug statement
            flash('Joined combat successfully!', 'success')
        else:
            print(f"Character {character.name} is already in the combat {combat.name}")  # Debug statement
            flash('Character is already in the combat.', 'warning')
    else:
        print(f"Failed to join combat {combat.name} for character {character.name}")  # Debug statement
        flash('Failed to join combat.', 'danger')
    return redirect(url_for('combats.view_combats', campaign_id=campaign.id))

@combats_bp.route('/<int:combat_id>/leave', methods=['POST'])
@login_required
def leave_combat(combat_id):
    combat = Combat.get_by_id(combat_id)
    campaign = Campaign.get_by_id(combat.campaign_id)
    character = Character.get_by_user_and_campaign(current_user.id, campaign.name)
    if character:
        if character.id in combat.participants:
            combat.remove_participant(character)
            redis_client.srem(f"combat:{combat_id}:participants", character.id)
            print(f"Character {character.name} left combat {combat.name}")  # Debug statement
            flash('Left combat successfully!', 'success')
        else:
            print(f"Character {character.name} is not in the combat {combat.name}")  # Debug statement
            flash('Character is not in the combat.', 'warning')
    else:
        print(f"Failed to leave combat {combat.name} for character {character.name}")  # Debug statement
        flash('Failed to leave combat.', 'danger')
    return redirect(url_for('combats.view_combats', campaign_id=campaign.id))

@combats_bp.route('/<int:combat_id>/fight', methods=['GET', 'POST'])
@login_required
def fight_combat(combat_id):
    combat = Combat.get_by_id(combat_id)
    campaign = Campaign.get_by_id(combat.campaign_id)
    if request.method == 'POST':
        participants_data = request.json.get('participants', [])
        redis_client.hmset(f"combat:{combat_id}", {
            "participants_data": participants_data
        })
        return jsonify({"message": "Participants saved successfully"})
    
    participants_data = redis_client.hget(f"combat:{combat_id}", "participants_data")
    if participants_data is None:
        participants_data = []

    return render_template('combats/fight.html', combat=combat, campaign=campaign, participants_data=participants_data)

@combats_bp.route('/<int:combat_id>/save_state', methods=['POST'])
@login_required
def save_state(combat_id):
    combat = Combat.get_by_id(combat_id)
    participants_data = request.json.get('participants', [])
    redis_client.hmset(f"combat:{combat_id}", {
        "participants_data": participants_data
    })
    return jsonify({"message": "Combat state saved successfully"})

@combats_bp.route('/<int:combat_id>/delete_state', methods=['POST'])
@login_required
def delete_state(combat_id):
    combat = Combat.get_by_id(combat_id)
    if combat:
        initial_participants = [
            {
                'name': participant.name,
                'remainingHP': participant.hit_points,
                'totalHP': participant.hit_points
            }
            for participant in combat.participants
        ]
        redis_client.hmset(f"combat:{combat_id}", {
            "participants_data": initial_participants
        })
        return jsonify({'success': True, 'message': 'Combat state reset to initial participants successfully.'})
    return jsonify({'success': False, 'message': 'Combat not found.'})

@combats_bp.route('/combats', methods=['GET'])
def list_combats():
    combats = Combat.get_all()
    return render_template('combats/list.html', combats=combats)

@combats_bp.route('/<int:campaign_id>/view_combats', methods=['GET'])
@login_required
def view_combats(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    combats = Combat.get_all_by_campaign(campaign_id)
    characters = Character.get_by_username(current_user.username)
    # Ensure each combat has unique participants
    for combat in combats:
        combat.participants = list(set(combat.participants))
        print(f"Combat {combat.name} participants: {combat.participants}")  # Debug statement
    return render_template('combats/view_combats.html', campaign=campaign, combats=combats, characters=characters)

@combats_bp.route('/<int:combat_id>/start_fight', methods=['GET'])
@login_required
def start_fight_combat(combat_id):
    combat = Combat.get_by_id(combat_id)
    campaign = Campaign.get_by_id(combat.campaign_id)
    participants_data = redis_client.hget(f"combat:{combat_id}", "participants_data")
    if participants_data is None:
        participants_data = []
    return render_template('combats/fight.html', combat=combat, campaign=campaign, participants_data=participants_data)