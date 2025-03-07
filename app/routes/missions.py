from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.mission import Mission
from app.models.campaign import Campaign

missions_bp = Blueprint('missions', __name__)

@missions_bp.route('/<int:campaign_id>/manage', methods=['GET', 'POST'])
@login_required
def manage_missions(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to manage missions for this campaign.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign_id))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_mission = Mission(name=name, description=description, campaign_id=campaign_id)
        db.session.add(new_mission)
        db.session.commit()
        flash('Mission created successfully!', 'success')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign_id))
    
    missions = Mission.query.filter_by(campaign_id=campaign_id).all()
    return render_template('missions/manage.html', campaign=campaign, missions=missions)

@missions_bp.route('/<int:mission_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    campaign = Campaign.query.get_or_404(mission.campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to edit this mission.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    if request.method == 'POST':
        mission.name = request.form['name']
        mission.description = request.form['description']
        mission.rewards = request.form['rewards']
        db.session.commit()
        flash('Mission updated successfully!', 'success')
        return redirect(url_for('missions.manage_missions', campaign_id=campaign.id))
    
    return render_template('missions/edit.html', mission=mission)

@missions_bp.route('/<int:mission_id>/delete', methods=['POST'])
@login_required
def delete_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    campaign = Campaign.query.get_or_404(mission.campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to delete this mission.', 'danger')
        return redirect(url_for('campaigns.play_campaign', campaign_id=campaign.id))

    db.session.delete(mission)
    db.session.commit()
    flash('Mission deleted successfully!', 'success')
    return redirect(url_for('missions.manage_missions', campaign_id=campaign.id))

@missions_bp.route('/<int:campaign_id>/view', methods=['GET'])
@login_required
def view_missions(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    missions = Mission.query.filter_by(campaign_id=campaign_id).all()
    return render_template('missions/view.html', campaign=campaign, missions=missions)

@missions_bp.route('/vote/<int:mission_id>', methods=['POST'])
@login_required
def vote_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    mission.vote(current_user)
    flash('Voted successfully!', 'success')
    return redirect(url_for('missions.view_missions', campaign_id=mission.campaign_id))

@missions_bp.route('/unvote/<int:mission_id>', methods=['POST'])
@login_required
def unvote_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    mission.unvote(current_user)
    flash('Vote removed successfully!', 'success')
    return redirect(url_for('missions.view_missions', campaign_id=mission.campaign_id))

@missions_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_mission():
    if request.method == 'POST':
        name = request.form['name']
        new_mission = Mission(name=name, creator_id=current_user.id)
        db.session.add(new_mission)
        db.session.commit()
        flash('Mission created successfully!', 'success')
        return redirect(url_for('missions.list_missions'))
    return render_template('missions/create.html')

@missions_bp.route('/')
@login_required
def list_missions():
    missions = Mission.query.filter_by(creator_id=current_user.id).all()
    return render_template('missions/list.html', missions=missions)
