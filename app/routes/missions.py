from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.mission import Mission
from app.models.campaign import Campaign
from app import db

missions_bp = Blueprint('missions', __name__)

@missions_bp.route('/missions/<campaign_id>/view')
@login_required
def view_missions(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaña no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    missions = Mission.get_by_campaign(campaign.name)
    return render_template('missions/view.html', campaign=campaign, missions=missions)

@missions_bp.route('/missions/<campaign_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_missions(campaign_id):
    if current_user.role != 'master':
        flash('Solo los masters pueden gestionar campañas', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaña no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        mission_name = request.form.get('name')
        mission_description = request.form.get('description')
        mission_rewards = request.form.get('rewards', 0)

        Mission.create(
            name=mission_name,
            description=mission_description,
            campaign_name=campaign.name,
            rewards=mission_rewards
        )
        flash('Misión creada con éxito', 'success')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign._id))

    missions = Mission.get_by_campaign(campaign.name)
    return render_template('missions/manage.html', campaign=campaign, missions=missions)

@missions_bp.route('/missions/<campaign_id>/edit/<mission_id>', methods=['GET', 'POST'])
@login_required
def edit_mission(campaign_id, mission_id):
    if current_user.role != 'master':
        flash('Solo los mastes pueden editar misiones', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaña no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    mission = Mission.get_by_id(mission_id)
    if not mission:
        flash('Misión no encontrada', 'danger')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign._id))

    if request.method == 'POST':
        mission.name = request.form.get('name')
        mission.description = request.form.get('description')
        mission.rewards = request.form.get('rewards', 0)
        db.save(mission)
        flash('Misión actualizada con éxito', 'success')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign._id))

    return render_template('missions/edit.html', campaign=campaign, mission=mission)

@missions_bp.route('/missions/delete/<campaign_id>/<mission_id>', methods=['POST'])
@login_required
def delete_mission(campaign_id, mission_id):
    mission = Mission.get_by_id(mission_id)
    if not mission:
        flash('Misión no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    # Get the campaign by ID instead of name
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaña no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if hasattr(mission, '_id') and mission._id:
        db.delete(mission._id)
        flash('Misión borrada con éxito', 'success')
    else:
        flash('Misión no tiene un ID válido', 'danger')
    
    # Redirect back to manage missions using the campaign_id from the URL
    return redirect(url_for('missions.manage_missions', campaign_id=campaign_id))

@missions_bp.route('/vote/<mission_id>', methods=['POST'])
@login_required
def vote_mission(mission_id):
    if not mission_id:
        flash('Misión no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    mission = Mission.get_by_id(mission_id)
    
    if not mission:
        flash('Misión no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    mission.vote(current_user)
    
    campaign = Campaign.get_by_name(mission.campaign_name)
    if not campaign:
        flash('Campaña no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
        
    flash('Votación exitosa', 'success')
    return redirect(url_for('missions.view_missions', campaign_id=campaign._id))

@missions_bp.route('/unvote/<mission_id>', methods=['POST'])
@login_required
def unvote_mission(mission_id):
    if not mission_id:
        flash('Misión no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    mission = Mission.get_by_id(mission_id)
    
    if not mission:
        flash('Misión no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    mission.unvote(current_user)
    
    campaign = Campaign.get_by_name(mission.campaign_name)
    if not campaign:
        flash('Campaña no encontrada', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
        
    flash('Voto eliminado con éxito', 'success')
    return redirect(url_for('missions.view_missions', campaign_id=campaign._id))

@missions_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_mission():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        rewards = request.form.get('rewards', '')
        new_mission = Mission.create(name, description, rewards)
        flash('Misión creada con éxito', 'success')
        return redirect(url_for('missions.list_missions'))
    return render_template('missions/create.html')

@missions_bp.route('/')
@login_required
def list_missions():
    missions = Mission.get_all()
    return render_template('missions/view.html', missions=missions, campaign=None)
