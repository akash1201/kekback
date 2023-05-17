from urllib import request
from flask import Blueprint
from flask import jsonify, request, abort, make_response
from AC.database.models import Attachments, Users, UserWeapon, WeaponAttachment, Weapons
from AC.routes.auth import token_required
from .. import db

users = Blueprint('users', __name__)

# Get weapons associated with a user
@token_required
@users.route('/user/<int:user_id>/weapons', methods=['GET'])
def get_user_weapons(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    weapons = []
    for association in user.weapon_associations:
        weapons.append(association.weapon.as_dict())

    return jsonify(weapons)


# Get users associated with a weapon
@token_required
@users.route('/weapon/<int:weapon_id>/users', methods=['GET'])
def get_weapon_users(weapon_id):
    weapon = Weapons.query.get(weapon_id)
    if not weapon:
        return jsonify({'message': 'Weapon not found'}), 404

    users = []
    for association in weapon.user_associations:
        users.append(association.user.as_dict())

    return jsonify(users)


# Add association between a user and a weapon
@token_required
@users.route('/user/<int:user_id>/weapon/<int:weapon_id>', methods=['POST'])
def add_user_weapon_association(user_id, weapon_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    weapon = Weapons.query.get(weapon_id)
    if not weapon:
        return jsonify({'message': 'Weapon not found'}), 404

    association = UserWeapon(user=user, weapon=weapon)
    db.session.add(association)
    db.session.commit()

    return jsonify({'message': 'Association added successfully'}), 201


# Delete association between a user and a weapon
@token_required
@users.route('/user/<int:user_id>/weapon/<int:weapon_id>', methods=['DELETE'])
def delete_user_weapon_association(user_id, weapon_id):
    association = UserWeapon.query.filter_by(user_id=user_id, weapon_id=weapon_id).first()
    if not association:
        return jsonify({'message': 'Association not found'}), 404

    db.session.delete(association)
    db.session.commit()

    return jsonify({'message': 'Association deleted successfully'}), 200
