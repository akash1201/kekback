from urllib import request
from flask import Blueprint
from flask import jsonify, request, abort, make_response
from AC.database.models import Characters, CharacterOutfit, Outfits, UserCharacter
from AC.routes.auth import token_required
from .. import db
characters = Blueprint('characters', __name__)

# Routes for the Characters model
# Route to get all characters
@characters.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters.query.all()
    return jsonify([character.as_dict() for character in characters])


# Route to get unique character categories
@characters.route('/character-categories')
def get_character_categories():
    character_categories = db.session.query(Characters.category).distinct().all()
    character_categories = [category[0] for category in character_categories]
    return jsonify(character_categories)


# Route to get a specific character by ID
@characters.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get_or_404(character_id)
    return jsonify(character.as_dict())

# Route to create a new character
@characters.route('/characters', methods=['POST'])
def create_character():
    data = request.get_json()
    character = Characters(name=data['name'], category=data['category'], modelUrl=data['modelUrl'], 
                           miniModelUrl=data['miniModelUrl'], custom=data['custom'], minRequiredOutfits = data['minRequiredOutfits'])
    db.session.add(character)
    db.session.commit()
    return jsonify(character.as_dict())

# Route to update an existing character by ID
@characters.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    character = Characters.query.get_or_404(character_id)
    data = request.get_json()
    character.name = data['name']
    character.category = data['category']
    character.modelUrl = data['modelUrl']
    character.miniModelUrl = data['miniModelUrl']
    character.custom = data['custom']
    character.minRequiredOutfits = data['minRequiredOutfits']
    db.session.commit()
    return jsonify(character.as_dict())

# Route to delete an existing character by ID
@characters.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get_or_404(character_id)
    db.session.delete(character)
    db.session.commit()
    return '', 204


@characters.route('/characters/<character_type>/unique_outfit_type', methods=['GET'])
def get_character_outfit_types(character_type):
    outfit_types = db.session.query(CharacterOutfit.outfit_type).join(Characters).join(Outfits).filter(Characters.id == character_type).distinct().all()
    outfit_types = [outfit_type[0] for outfit_type in outfit_types]
    if not outfit_types:
        return []
    return jsonify(outfit_types)




# Routes for the outfit model
# Get all outfits
@characters.route('/outfits', methods=['GET'])
def get_all_outfits():
    outfits = Outfits.query.all()
    return jsonify([outfit.as_dict() for outfit in outfits]), 200

# Get outfit by id
@characters.route('/outfits/<int:outfit_id>', methods=['GET'])
def get_outfit_by_id(outfit_id):
    outfit = Outfits.query.get(outfit_id)
    if not outfit:
        return jsonify({'message': 'outfit not found.'}), 404
    return jsonify(outfit.as_dict()), 200

# Create a new outfit
@characters.route('/outfits', methods=['POST'])
def create_new_outfit():
    data = request.get_json()
    name = data.get('name')
    type = data.get('type')
    if not name or not type:
        return jsonify({'message': 'Name and type are required fields.'}), 400
    outfit = Outfits(name=name, type=type)
    db.session.add(outfit)
    db.session.commit()
    return jsonify(outfit.as_dict()), 201

# Update an existing outfit
@characters.route('/outfits/<int:outfit_id>', methods=['PUT'])
def update_outfit(outfit_id):
    data = request.get_json()
    outfit = Outfits.query.get(outfit_id)
    if not outfit:
        return jsonify({'message': 'outfit not found.'}), 404
    if 'name' in data:
        outfit.name = data['name']
    if 'type' in data:
        outfit.type = data['type']
    db.session.commit()
    return jsonify(outfit.as_dict()), 200

# Delete a outfit
@characters.route('/outfits/<int:outfit_id>', methods=['DELETE'])
def delete_outfit(outfit_id):
    outfit = Outfits.query.get(outfit_id)
    if not outfit:
        return jsonify({'message': 'outfit not found.'}), 404
    db.session.delete(outfit)
    db.session.commit()
    return jsonify({'message': 'outfit deleted.'}), 200








# Routes for the CharacterOutfit model
# Get all outfits for a given character
@characters.route('/characters/<int:character_id>/outfits', methods=['GET'])
def get_all_outfits_for_character(character_id):
    outfits =  db.session.query(Outfits).join(
        CharacterOutfit, Outfits.id == CharacterOutfit.outfit_id
    ).filter(
        CharacterOutfit.character_id == character_id
    ).distinct().all()
    results = [outfit.as_dict() for outfit in outfits]
    if not results:
        return jsonify([])
    return jsonify(results)




# Create a outfit for a given character
@token_required
@characters.route('/characters_outfits', methods=['POST'])
def create_outfit_for_character():
    data = request.get_json()
    character_name = data['character_name']
    outfit_name = data['outfit_name']

    character = Characters.query.filter_by(name=character_name).first()
    if not character:
        return jsonify({'message': 'Character not found'}), 604

    outfit = Outfits.query.filter_by(name=outfit_name).first()
    if not outfit:
        return jsonify({'message': 'Outfit not found'}), 604

    character_outfit = CharacterOutfit(character_id=character.id, outfit_id=outfit.id, outfit_type=outfit.type)
    db.session.add(character_outfit)
    db.session.commit()

    return jsonify(character_outfit.as_dict())



# Delete a outfit for a given character
@token_required
@characters.route('/characters/<int:character_id>/outfits/<int:outfit_id>', methods=['DELETE'])
def delete_outfit_for_character(character_id, outfit_id):
    character_outfit = CharacterOutfit.query.filter_by(character_id=character_id, outfit_id=outfit_id).first_or_404()
    db.session.delete(character_outfit)
    db.session.commit()
    return jsonify({"Status":"Success"}), 204



# Routes for the UserCharacter model
#Get all characters associated with a user.
@characters.route('/users/<int:user_id>/characters', methods=['GET'])
def get_all_characters_for_user(user_id):
    user_characters = UserCharacter.query.filter_by(user_id=user_id)
    return jsonify([user_character.characters.as_dict() for user_character in user_characters])

#Get a specific character associated with a user.
@characters.route('/users/<int:user_id>/characters/<int:character_id>', methods=['GET'])
def get_character_for_user(user_id, character_id):
    user_character = UserCharacter.query.filter_by(user_id=user_id, character_id=character_id).first_or_404()
    return jsonify(user_character.characters.as_dict())

#Add a character to a user's list of characters.
@token_required
@characters.route('/users/<int:user_id>/characters', methods=['POST'])
def add_character_to_user(user_id):
    data = request.get_json()
    character = Characters.query.get_or_404(data['character_id'])
    user_character = UserCharacter(user_id=user_id, character_id=data['character_id'], outfit=data['outfit'],
                                    default=data['default'])
    db.session.add(user_character)
    db.session.commit()
    return jsonify(user_character.as_dict())

#Update a specific character associated with a user.
@token_required
@characters.route('/users/<int:user_id>/characters/<int:character_id>', methods=['PUT'])
def update_character_for_user(user_id, character_id):
    user_character = UserCharacter.query.filter_by(user_id=user_id, character_id=character_id).first_or_404()
    data = request.get_json()
    user_character.outfit = data['outfit']
    user_character.default = data['default']
    db.session.commit()
    return jsonify(user_character.as_dict())

#Delete a specific character associated with a user.
@token_required
@characters.route('/users/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def delete_character_for_user(user_id, character_id):
    user_character = UserCharacter.query.filter_by(user_id=user_id, character_id=character_id).first_or_404()
    db.session.delete(user_character)
    db.session.commit()
    return jsonify({"Status":"Success"}), 204
