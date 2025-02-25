from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.models.user import User
from app.models.character import Character
from app import db

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/')
@login_required
def list_campaigns():
    if current_user.role == 'master':
        campaigns = Campaign.query.filter_by(master_id=current_user.id).all()
    else:
        campaigns = Campaign.query.filter(
            (Campaign.is_public == True) | 
            (Campaign.allowed_players.any(id=current_user.id))
        ).all()
    return render_template('campaigns/list.html', campaigns=campaigns)

@campaigns_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if current_user.role != 'master':
        flash('You do not have permission to create a campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

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
        campaign.allowed_players = [User.query.get(int(player_id)) for player_id in allowed_players]
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
    if not campaign.is_public and current_user not in campaign.allowed_players and campaign.master_id != current_user.id:
        flash('You do not have permission to view this campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    allowed_players = campaign.allowed_players
    character = Character.query.filter_by(user_id=current_user.id, campaign_id=campaign.id).first()
    return render_template('campaigns/view.html', campaign=campaign, allowed_players=allowed_players, character=character)

@campaigns_bp.route('/join/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def join_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if request.method == 'POST':
        character_id = request.form.get('character_id')
        character = Character.query.get_or_404(character_id)
        if character.user_id != current_user.id:
            flash('You do not have permission to join this campaign with this character.', 'danger')
            return redirect(url_for('campaigns.list_campaigns'))
        character.campaign_id = campaign.id
        db.session.commit()
        flash('Joined campaign successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    
    characters = Character.query.filter_by(user_id=current_user.id, campaign_id=None).all()
    return render_template('campaigns/join.html', campaign=campaign, characters=characters)

@campaigns_bp.route('/leave/<int:campaign_id>', methods=['POST'])
@login_required
def leave_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    character = Character.query.filter_by(user_id=current_user.id, campaign_id=campaign.id).first()
    if character:
        character.campaign_id = None
        db.session.commit()
        flash('Left campaign successfully!', 'success')
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/play/<int:campaign_id>', methods=['GET'])
@login_required
def play_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    character = Character.query.filter_by(user_id=current_user.id, campaign_id=campaign.id).first()
    if not character and current_user.role != 'master':
        flash('You do not have a character in this campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/play.html', campaign=campaign)