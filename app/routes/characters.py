from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.character import Character
from app import db

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/')
@login_required
def list_characters():
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return render_template('characters/list.html', characters=characters)

@characters_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_character():
    if request.method == 'POST':
        name = request.form['name']
        new_character = Character(name=name, user_id=current_user.id)
        db.session.add(new_character)
        db.session.commit()
        flash('Character created successfully!', 'success')
        return redirect(url_for('characters.list_characters'))
    return render_template('characters/new.html')

@characters_bp.route('/edit/<int:character_id>', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
    character = Character.query.get_or_404(character_id)
    if character.player_id != current_user.id:
        flash('You do not have permission to edit this character.', 'danger')
        return redirect(url_for('characters.list_characters'))

    if request.method == 'POST':
        character.name = request.form.get('name')
        db.session.commit()
        flash('Character updated successfully!', 'success')
        return redirect(url_for('characters.list_characters'))
    
    return render_template('characters/edit.html', character=character)

@characters_bp.route('/')
def characters_index():
    return render_template('characters/index.html')