from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.character import Character

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/characters', methods=['GET'])
@login_required
def character_list():
    characters = Character.query.filter_by(player_id=current_user.id).all()
    return render_template('characters/list.html', characters=characters)

@characters_bp.route('/characters/new', methods=['GET', 'POST'])
@login_required
def new_character():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_character = Character(name=name, player_id=current_user.id)
            new_character.save()
            flash('Character created successfully!', 'success')
            return redirect(url_for('characters.character_list'))
        flash('Character name is required!', 'danger')
    return render_template('characters/new.html')

@characters_bp.route('/characters/edit/<int:character_id>', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
    character = Character.query.get_or_404(character_id)
    if character.player_id != current_user.id:
        flash('You do not have permission to edit this character.', 'danger')
        return redirect(url_for('characters.character_list'))

    if request.method == 'POST':
        character.name = request.form.get('name')
        character.save()
        flash('Character updated successfully!', 'success')
        return redirect(url_for('characters.character_list'))
    
    return render_template('characters/edit.html', character=character)