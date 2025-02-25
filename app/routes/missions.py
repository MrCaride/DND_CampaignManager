from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.mission import Mission
from app.models.campaign import Campaign
from app import db

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

@missions_bp.route('/<int:campaign_id>/view', methods=['GET'])
@login_required
def view_missions(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    missions = Mission.query.filter_by(campaign_id=campaign_id).all()
    return render_template('missions/view.html', campaign=campaign, missions=missions)
