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
        race = request.form['race']
        character_class = request.form['character_class']
        level = request.form.get('level', 1) or 1
        strength = request.form.get('strength', 10) or 1
        dexterity = request.form.get('dexterity', 10) or 1
        constitution = request.form.get('constitution', 10) or 1
        intelligence = request.form.get('intelligence', 10) or 1
        wisdom = request.form.get('wisdom', 10) or 1
        charisma = request.form.get('charisma', 10) or 1
        hit_points = request.form.get('hit_points', 10) or 1
        armor_class = request.form.get('armor_class', 10) or 1
        initiative = request.form.get('initiative', 0) or 1
        speed = request.form.get('speed', 30) or 1
        
        if not name or not race or not character_class:
            flash('Name, race, and class are required fields.', 'danger')
            return redirect(url_for('characters.new_character'))
        
        new_character = Character(
            name=name, user_id=current_user.id, race=race, character_class=character_class,
            level=level, strength=strength, dexterity=dexterity, constitution=constitution,
            intelligence=intelligence, wisdom=wisdom, charisma=charisma, hit_points=hit_points,
            armor_class=armor_class, initiative=initiative, speed=speed
        )
        db.session.add(new_character)
        db.session.commit()
        flash('Character created successfully!', 'success')
        return redirect(url_for('characters.list_characters'))
    return render_template('characters/new.html')

@characters_bp.route('/edit/<int:character_id>', methods=['GET', 'POST'])
@login_required
def edit_character(character_id):
    character = Character.query.get_or_404(character_id)
    if character.user_id != current_user.id:
        flash('You do not have permission to edit this character.', 'danger')
        return redirect(url_for('characters.list_characters'))

    if request.method == 'POST':
        character.name = request.form.get('name')
        character.race = request.form.get('race')
        character.character_class = request.form.get('character_class')
        character.level = request.form.get('level') or 1
        character.strength = request.form.get('strength') or 1
        character.dexterity = request.form.get('dexterity') or 1
        character.constitution = request.form.get('constitution') or 1
        character.intelligence = request.form.get('intelligence') or 1
        character.wisdom = request.form.get('wisdom') or 1
        character.charisma = request.form.get('charisma') or 1
        character.hit_points = request.form.get('hit_points') or 1
        character.armor_class = request.form.get('armor_class') or 1
        character.initiative = request.form.get('initiative') or 1
        character.speed = request.form.get('speed') or 1
        db.session.commit()
        flash('Character updated successfully!', 'success')
        return redirect(url_for('characters.list_characters'))
    
    return render_template('characters/edit.html', character=character)

@characters_bp.route('/delete/<int:character_id>', methods=['POST'])
@login_required
def delete_character(character_id):
    character = Character.query.get_or_404(character_id)
    if character.user_id != current_user.id:
        flash('You do not have permission to delete this character.', 'danger')
        return redirect(url_for('characters.list_characters'))
    
    db.session.delete(character)
    db.session.commit()
    flash('Character deleted successfully!', 'success')
    return redirect(url_for('characters.list_characters'))

@characters_bp.route('/view/<int:character_id>', methods=['GET'])
@login_required
def view_character(character_id):
    character = Character.query.get_or_404(character_id)
    if character.user_id != current_user.id:
        flash('You do not have permission to view this character.', 'danger')
        return redirect(url_for('characters.list_characters'))
    
    return render_template('characters/view.html', character=character)