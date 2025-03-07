from flask import Blueprint, render_template, request, redirect, url_for
from app.models.character import Character

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/characters', methods=['GET'])
def list_characters():
    characters = Character.get_all()
    return render_template('characters/list.html', characters=characters)

@characters_bp.route('/characters/create', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        name = request.form.get('name')
        race = request.form.get('race')
        character_class = request.form.get('character_class')
        level = request.form.get('level')
        Character.create(name, race, character_class, level)
        return redirect(url_for('characters.list_characters'))
    return render_template('characters/create.html')