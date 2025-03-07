from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.models.user import User
from app.models.character import Character
from app.models.mission import Mission
from app.models.combat import Combat
from app import redis_client

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/')
@login_required
def list_campaigns():
    if current_user.role == 'master':
        campaigns = [campaign for campaign in Campaign.get_all() if campaign.master_id == current_user.id]
        print(f"Master {current_user.username} campaigns: {[campaign.name for campaign in campaigns]}")  # Debug statement
    else:
        campaigns = [campaign for campaign in Campaign.get_all() if campaign.is_public or current_user.username in campaign.allowed_players]
        print(f"Player {current_user.username} campaigns: {[campaign.name for campaign in campaigns]}")  # Debug statement
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
        new_campaign = Campaign.create(name=name, is_public=is_public, master_id=current_user.id)
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/create.html')

@campaigns_bp.route('/edit/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        campaign.name = request.form.get('name')
        campaign.is_public = 'is_public' in request.form
        redis_client.hmset(f"campaign:{campaign_id}", {
            "name": campaign.name,
            "is_public": int(campaign.is_public),
            "master_id": campaign.master_id
        })
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    
    players = User.get_all()
    return render_template('campaigns/edit.html', campaign=campaign, players=players)

@campaigns_bp.route('/delete/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    redis_client.delete(f"campaign:{campaign_id}")
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/view/<int:campaign_id>', methods=['GET'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    return render_template('campaigns/view.html', campaign=campaign)

@campaigns_bp.route('/join/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def join_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        character_id = request.form.get('character_id')
        character = Character.get_by_id(character_id)
        if character and character.user_id == current_user.id:
            flash('Joined campaign successfully!', 'success')
        else:
            flash('You do not have permission to join this campaign with this character.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    characters = Character.get_by_username(current_user.username)
    return render_template('campaigns/join.html', campaign=campaign, characters=characters)

@campaigns_bp.route('/leave/<int:campaign_id>', methods=['POST'])
@login_required
def leave_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    character = Character.get_by_username(current_user.username)
    if character:
        flash('Left campaign successfully!', 'success')
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/play/<int:campaign_id>', methods=['GET'])
@login_required
def play_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    characters = Character.get_all()
    missions = Mission.get_all()
    combats = Combat.get_all()
    if current_user.role == 'master':
        return render_template('campaigns/play_master.html', campaign=campaign, characters=characters, missions=missions, combats=combats)
    else:
        return render_template('campaigns/play_player.html', campaign=campaign, characters=characters, missions=missions, combats=combats)

@campaigns_bp.route('/operations_master/<int:campaign_id>', methods=['GET'])
@login_required
def operations_master(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/operations_master.html', campaign=campaign)

@campaigns_bp.route('/operations_player/<int:campaign_id>', methods=['GET'])
@login_required
def operations_player(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/operations_player.html', campaign=campaign)