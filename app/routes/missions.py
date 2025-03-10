from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.mission import Mission
from app.models.campaign import Campaign
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

missions_bp = Blueprint('missions', __name__)

@missions_bp.route('/<int:campaign_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_missions(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to manage missions for this campaign.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign_id))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        rewards = request.form.get('rewards', '')
        new_mission = Mission.create(name, description, campaign.name, rewards)
        flash('Mission created successfully!', 'success')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign_id))
    
    # Filter missions by campaign_name
    mission_ids = redis_client.keys("mission:*")
    missions = []
    for mission_id in mission_ids:
        mission = Mission.get_by_id(int(mission_id.split(b':')[1]))
        if mission and mission.campaign_name == campaign.name:
            missions.append(mission)
    
    return render_template('missions/manage.html', campaign=campaign, missions=missions)

@missions_bp.route('/<int:mission_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_mission(mission_id):
    mission = Mission.get_by_id(mission_id)
    campaign = Campaign.get_by_name(mission.campaign_name)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to edit this mission.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    if request.method == 'POST':
        mission.name = request.form['name']
        mission.description = request.form['description']
        mission.rewards = request.form.get('rewards', '')
        redis_client.hmset(f"mission:{mission_id}", {
            "name": mission.name,
            "description": mission.description,
            "campaign_name": mission.campaign_name,
            "rewards": mission.rewards,
            "votes": mission.votes
        })
        flash('Mission updated successfully!', 'success')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign.id))
    
    return render_template('missions/edit.html', mission=mission, campaign=campaign)

@missions_bp.route('/<int:mission_id>/delete', methods=['POST'])
@login_required
def delete_mission(mission_id):
    mission = Mission.get_by_id(mission_id)
    campaign = Campaign.get_by_name(mission.campaign_name)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to delete this mission.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    redis_client.delete(f"mission:{mission_id}")
    flash('Mission deleted successfully!', 'success')
    return redirect(url_for('missions.manage_missions', campaign_id=campaign.id))

@missions_bp.route('/<int:campaign_id>/view', methods=['GET'])
@login_required
def view_missions(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    # Obtener todas las misiones desde Redis
    mission_ids = redis_client.keys("mission:*")
    missions = []
    mission_ids_seen = set()
    for mission_id in mission_ids:
        mission = Mission.get_by_id(int(mission_id.split(b':')[1]))
        if mission and mission.campaign_name == campaign.name and mission.id not in mission_ids_seen:
            missions.append(mission)
            mission_ids_seen.add(mission.id)

    return render_template('missions/view.html', campaign=campaign, missions=missions)

@missions_bp.route('/vote/<int:mission_id>', methods=['POST'])
@login_required
def vote_mission(mission_id):
    mission = Mission.get_by_id(mission_id)
    mission.vote(current_user)
    campaign = Campaign.get_by_name(mission.campaign_name)
    flash('Voted successfully!', 'success')
    return redirect(url_for('missions.view_missions', campaign_id=campaign.id))

@missions_bp.route('/unvote/<int:mission_id>', methods=['POST'])
@login_required
def unvote_mission(mission_id):
    mission = Mission.get_by_id(mission_id)
    mission.unvote(current_user)
    campaign = Campaign.get_by_name(mission.campaign_name)
    flash('Vote removed successfully!', 'success')
    return redirect(url_for('missions.view_missions', campaign_id=campaign.id))

@missions_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_mission():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        rewards = request.form.get('rewards', '')
        new_mission = Mission.create(name, description, rewards)
        flash('Mission created successfully!', 'success')
        return redirect(url_for('missions.list_missions'))
    return render_template('missions/create.html')

@missions_bp.route('/')
@login_required
def list_missions():
    missions = Mission.get_all()
    return render_template('missions/list.html', missions=missions)
