from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.models.user import User
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
        is_public = 'is_public' in request.form
        new_campaign = Campaign(name=name, master_id=current_user.id, is_public=is_public)
        db.session.add(new_campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/create.html')

@campaigns_bp.route('/edit/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to edit this campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        campaign.name = request.form.get('name')
        campaign.is_public = 'is_public' in request.form
        allowed_players = request.form.getlist('allowed_players')
        campaign.allowed_players = [int(player_id) for player_id in allowed_players]
        db.session.commit()
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    
    players = User.query.all()
    return render_template('campaigns/edit.html', campaign=campaign, players=players)

@campaigns_bp.route('/delete/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.master_id != current_user.id:
        flash('You do not have permission to delete this campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/view/<int:campaign_id>', methods=['GET'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if not campaign.is_public and current_user.id not in campaign.allowed_players and campaign.master_id != current_user.id:
        flash('You do not have permission to view this campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    allowed_players = User.query.filter(User.id.in_(campaign.allowed_players)).all()
    return render_template('campaigns/view.html', campaign=campaign, allowed_players=allowed_players)