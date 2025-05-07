from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.character import Character
from app import db

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/characters', methods=['GET'])
@login_required
def list_characters():
    print(f"Fetching characters for user: {current_user.username}")
    characters = Character.get_by_username(current_user.username)
    print(f"Characters passed to template: {[(char.name, char.user_username) for char in characters]}")
    return render_template('characters/list.html', characters=characters)

@characters_bp.route('/characters/create', methods=['GET', 'POST'])
@login_required
def create_character():
    if request.method == 'POST':
        character = Character.create(
            name=request.form.get('name'),
            race=request.form.get('race'),
            character_class=request.form.get('character_class'),
            level=request.form.get('level'),
            user_id=current_user.id,
            user_username=current_user.username,
            strength=request.form.get('strength'),
            dexterity=request.form.get('dexterity'),
            constitution=request.form.get('constitution'),
            intelligence=request.form.get('intelligence'),
            wisdom=request.form.get('wisdom'),
            charisma=request.form.get('charisma'),
            armor_class=request.form.get('armor_class'),
            initiative=request.form.get('initiative'),
            hit_points=request.form.get('hit_points'),
            speed=request.form.get('speed')
        )
        print(f"Created character: {character.name} for user: {current_user.username}")
        return redirect(url_for('characters.list_characters'))
    return render_template('characters/create.html')

@characters_bp.route('/characters/view/<character_id>', methods=['GET'])
@login_required
def view_character(character_id):
    character = Character.get_by_id(character_id)
    if character and character.user_id == current_user.id:
        return render_template('characters/view.html', character=character)
    else:
        flash('You do not have permission to view this character.', 'danger')
        return redirect(url_for('characters.list_characters'))

@characters_bp.route('/characters/edit/<character_id>', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
    character = Character.get_by_id(character_id)
    if character and character.user_id == current_user.id:
        if request.method == 'POST':
            character.name = request.form.get('name')
            character.race = request.form.get('race')
            character.character_class = request.form.get('character_class')
            character.level = request.form.get('level')
            character.strength = request.form.get('strength')
            character.dexterity = request.form.get('dexterity')
            character.constitution = request.form.get('constitution')
            character.intelligence = request.form.get('intelligence')
            character.wisdom = request.form.get('wisdom')
            character.charisma = request.form.get('charisma')
            character.armor_class = request.form.get('armor_class')
            character.initiative = request.form.get('initiative')
            character.hit_points = request.form.get('hit_points')
            character.speed = request.form.get('speed')
            db.save(character)
            flash('Character updated successfully!', 'success')
            return redirect(url_for('characters.list_characters'))
        return render_template('characters/edit.html', character=character)
    else:
        flash('You do not have permission to edit this character.', 'danger')
        return redirect(url_for('characters.list_characters'))

@characters_bp.route('/characters/delete/<character_id>', methods=['POST'])
@login_required
def delete_character(character_id):
    character = Character.get_by_id(character_id)
    if character and character.user_id == current_user.id:
        # En Sirope, necesitamos mantener una referencia al objeto y borrarlo después
        db._r.delete(f"{db._Sirope__key_prefix}:{character.__class__.__name__}:{character.id}")
        flash('Character deleted successfully!', 'success')
    else:
        flash('You do not have permission to delete this character.', 'danger')
    return redirect(url_for('characters.list_characters'))