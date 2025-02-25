from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.models.mission import Mission
from app import db

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/')
@login_required
def list_campaigns():
    campaigns = Campaign.query.filter_by(master_id=current_user.id).all()
    return render_template('campaigns/list.html', campaigns=campaigns)

@campaigns_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if request.method == 'POST':
        name = request.form['name']
        new_campaign = Campaign(name=name, master_id=current_user.id)
        db.session.add(new_campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/create.html')

@campaigns_bp.route('/<int:campaign_id>', methods=['GET'])
@login_required
def view_campaign(campaign_id):
    campaign = redis_client.get(f'campaign:{campaign_id}')
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    missions = Mission.query.filter_by(campaign_id=campaign_id).all()
    return render_template('campaigns/view.html', campaign=campaign, missions=missions)

@campaigns_bp.route('/<int:campaign_id>/delete', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = redis_client.get(f'campaign:{campaign_id}')
    if campaign and campaign.master_id == current_user.id:
        redis_client.delete(f'campaign:{campaign_id}')
        flash('Campaign deleted successfully!', 'success')
    else:
        flash('You do not have permission to delete this campaign.', 'danger')
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/')
def campaigns_index():
    return render_template('campaigns/index.html')