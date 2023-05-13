from urllib import request
from AC.database.enums import WeaponsCategoryEnum, WeaponsTypeEnum
from flask import Blueprint
from flask import jsonify, request, abort, make_response
from AC.database.models import Attachments, Users, UserWeapon, WeaponAttachment, Weapons
from AC.routes.auth import token_required
from .. import db
weapons = Blueprint('weapons', __name__)

@weapons.route('/weapons', methods=['GET'])
def getWeapons():
        items = Weapons.query.all()
        print(items)
        wepons = []
        for item in items:
            wepons.append(item.as_dict())
        return jsonify(wepons)


@weapons.route('/weapon/<int:id>', methods=['GET'])
def getWeaponById(id):
    item = Weapons.query.get(id)
    if not item:
        abort(404)
    return jsonify(item.as_dict())


    
@weapons.route('/weapon/<int:id>/unique_attachment_type', methods=['GET'])
def getUniqueAttachmentsForWeaponById(id):
    attachments = db.session.query(Attachments.type).join(
        WeaponAttachment, Attachments.id == WeaponAttachment.attachment_id
    ).filter(
        WeaponAttachment.weapon_id == id
    ).distinct().all()
    results = [row[0] for row in attachments]
    print(results)
    if not results:
        return []
    return jsonify(results)



 
@weapons.route('/weapon/<int:id>/attachments', methods=['GET'])
def getAttachmentsForWeaponById(id):
    attachments = db.session.query(Attachments).join(
        WeaponAttachment, Attachments.id == WeaponAttachment.attachment_id
    ).filter(
        WeaponAttachment.weapon_id == id
    ).distinct().all()
    
    results = [attachment.as_dict() for attachment in attachments]
    if not results:
        return jsonify([])
    return jsonify(results)

@weapons.route('/weapon', methods=['POST'])
@token_required
def new_weapon(user):
    # Check if the request contains JSON data
    if not request.json:
        abort(400)

    # Check if the request contains valid values for category and type
    data = request.json
    if 'category' not in data or data['category'] not in WeaponsCategoryEnum.__members__:
        abort(400, 'Invalid category')
    if 'type' not in data or data['type'] not in WeaponsTypeEnum.__members__:
        abort(400, 'Invalid type')

    # Debug print to see the value of data['category']
    print(f"data['category'] = {data['category']}")

    # Create a new Weapons object using the validated values
    new_weapon = Weapons(
        name=data['name'],
        category=WeaponsCategoryEnum[data['category']],
        type=WeaponsTypeEnum[data['type']],
        subType=data['subType'],
        action=data['action'],
        ammo=data['ammo'],
        modelUrl=data['modelUrl'],
        miniModelUrl=data['miniModelUrl'],
        custom=data['custom']
    )

    # Debug print to see the value of new_weapon.category
    print(f"new_weapon.category = {new_weapon.category}")

    # Add the new weapon to the database and commit the transaction
    db.session.add(new_weapon)
    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        db.session.rollback()

    # Return the new weapon as a dictionary and set the response status code to 201
    return jsonify(new_weapon.as_dict()), 201


@weapons.route('/weapon/<int:weapon_id>', methods=['DELETE'])
@token_required
def removeWeapon(userid,weapon_id):
    weapon = Weapons.query.get(weapon_id)

    if not weapon:
        return jsonify({'error': f'weapon with id {weapon_id} does not exist'})

    WeaponAttachment.query.filter_by(weapon_id=weapon.id).delete()
    db.session.delete(weapon)
    db.session.commit()

    return jsonify({'message': f'weapon with id {weapon_id} and associated weapon attachments have been deleted'})
