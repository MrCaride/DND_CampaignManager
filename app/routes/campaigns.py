from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.models.user import User
from app.models.character import Character
from app.models.mission import Mission
from app import db

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/')
@login_required
def list_campaigns():
    if current_user.role == 'master':
        campaigns = list(db.filter(Campaign, lambda c: str(c.master_id) == str(current_user._oid)))
        print(f"Master {current_user.username} campaigns: {[campaign.name for campaign in campaigns]}")
    else:
        all_campaigns = Campaign.get_all()
        campaigns = [campaign for campaign in all_campaigns 
                    if campaign.is_public or current_user.username in campaign.allowed_players]
        print(f"Player {current_user.username} campaigns: {[campaign.name for campaign in campaigns]}")

    user_characters = Character.get_by_username(current_user.username)
    joined_campaigns = {character.campaign: character for character in user_characters if character.campaign}
    print(f"User {current_user.username} joined campaigns: {joined_campaigns}")

    joined_campaigns = {campaign_name: character for campaign_name, character in joined_campaigns.items() 
                       if campaign_name in [campaign.name for campaign in campaigns]}
    print(f"Filtered joined campaigns: {joined_campaigns}")

    return render_template('campaigns/list.html', campaigns=campaigns, joined_campaigns=joined_campaigns)

@campaigns_bp.route('/view/<campaign_id>', methods=['GET'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    characters = Character.get_by_username(current_user.username)
    return render_template('campaigns/view.html', campaign=campaign, characters=characters)

@campaigns_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if current_user.role != 'master':
        flash('You do not have permission to create a campaign.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        name = request.form['name']
        is_public = 'is_public' in request.form
        new_campaign = Campaign.create(name=name, is_public=is_public, master_id=str(current_user._oid))
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    return render_template('campaigns/create.html')

@campaigns_bp.route('/edit/<campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        campaign.name = request.form.get('name')
        campaign.is_public = 'is_public' in request.form
        # Obtener la lista de allowed_players
        campaign.allowed_players = request.form.getlist('allowed_players')
        print(f"Updating campaign {campaign.name} with allowed players: {campaign.allowed_players}")
        db.save(campaign)
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('campaigns.list_campaigns'))
    
    players = [user for user in User.get_all() if user.role != 'master']
    return render_template('campaigns/edit.html', campaign=campaign, players=players)

@campaigns_bp.route('/delete/<campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    if hasattr(campaign, '_id') and campaign._id:
        db.delete(campaign._id)  # Pass the OID instead of the object
        flash('Campaign deleted successfully!', 'success')
    else:
        flash('Campaign does not have a valid ID.', 'danger')
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/join/<campaign_id>', methods=['GET', 'POST'])
@login_required
def join_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))

    if request.method == 'POST':
        character_id = request.form.get('character_id')
        character = Character.get_by_id(character_id)
        if character and str(character.user_id) == str(current_user._oid):  # Compare using _oid
            if character.campaign:
                flash('This character is already in another campaign.', 'danger')
                return redirect(url_for('campaigns.list_campaigns'))
            character.campaign = campaign.name
            db.save(character)
            flash('Joined campaign successfully!', 'success')
        else:
            flash('You do not have permission to join this campaign with this character.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    characters = Character.get_by_username(current_user.username)
    return render_template('campaigns/join.html', campaign=campaign, characters=characters)

@campaigns_bp.route('/leave/<campaign_id>', methods=['POST'])
@login_required
def leave_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    character = Character.get_by_user_and_campaign(str(current_user._oid), campaign.name)  # Use _oid
    if character:
        character.campaign = None
        character.campaign_id = None
        db.save(character)
        flash('Left campaign successfully!', 'success')
    else:
        flash('You are not part of this campaign.', 'danger')
    
    return redirect(url_for('campaigns.list_campaigns'))

@campaigns_bp.route('/play/<campaign_id>', methods=['GET'])
@login_required
def play_campaign(campaign_id):
    campaign = Campaign.get_by_id(campaign_id)
    if not campaign:
        flash('Campaign not found.', 'danger')
        return redirect(url_for('campaigns.list_campaigns'))
    
    characters = Character.get_all()
    campaign_characters = [character for character in characters if character.campaign == campaign.name]
    print(f"Characters in this campaign: {[(char.name, char.user_username) for char in campaign_characters]}")

    missions = Mission.get_by_campaign(campaign.name)
    if current_user.role == 'master':
        return render_template('campaigns/play_master.html', campaign=campaign, characters=campaign_characters, missions=missions)
    else:
        return render_template('campaigns/play_player.html', campaign=campaign, characters=campaign_characters, missions=missions)