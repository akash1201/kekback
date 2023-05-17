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
    # Get all weapons from the database
    items = Weapons.query.all()
    print(items)
    wepons = []
    for item in items:
        wepons.append(item.as_dict())
    return jsonify(wepons)


@weapons.route('/weapons/<int:id>', methods=['GET'])
def getWeaponById(id):
    # Get a weapon by its ID from the database
    item = Weapons.query.get(id)
    if not item:
        abort(404)
    return jsonify(item.as_dict())


@weapons.route('/weapons/<int:id>/unique_attachment_type', methods=['GET'])
def getUniqueAttachmentsForWeaponById(id):
    # Get unique attachment types for a weapon by its ID
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


@weapons.route('/weapons/<int:id>/attachments', methods=['GET'])
def getAttachmentsForWeaponById(id):
    # Get attachments for a weapon by its ID
    attachments = db.session.query(Attachments).join(
        WeaponAttachment, Attachments.id == WeaponAttachment.attachment_id
    ).filter(
        WeaponAttachment.weapon_id == id
    ).distinct().all()

    results = [attachment.as_dict() for attachment in attachments]
    if not results:
        return jsonify([])
    return jsonify(results)


@weapons.route('/weapons', methods=['POST'])
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
    db.session.commit()

    # Return the new weapon as a dictionary and set the response status code to 201
    return jsonify(new_weapon.as_dict()), 201


@weapons.route('/weapons/<int:weapon_id>', methods=['DELETE'])
@token_required
def removeWeapon(userid,weapon_id):
    weapon = Weapons.query.get(weapon_id)

    if not weapon:
        return jsonify({'error': f'weapon with id {weapon_id} does not exist'})

    WeaponAttachment.query.filter_by(weapon_id=weapon.id).delete()
    db.session.delete(weapon)
    db.session.commit()

    return jsonify({'message': f'weapon with id {weapon_id} and associated weapon attachments have been deleted'})



@weapons.route('/attachments', methods=['GET'])
def getAttachments():
    attachments = Attachments.query.all()
    attachments_dict = [attachment.as_dict() for attachment in attachments]
    return jsonify(attachments_dict), 200


@weapons.route('/attachments', methods=['POST'])
def createAttachment():
    # Create a new attachment
    data = request.json
    name = data.get('name')
    type = data.get('type')

    # Validate the input
    if not name or not type:
        abort(400, 'Name and type are required')

    attachment = Attachments(name=name, type=type)
    db.session.add(attachment)
    db.session.commit()

    return jsonify(attachment.as_dict()), 201


@weapons.route('/attachments/<int:id>', methods=['PUT'])
@token_required
def updateAttachment(id):
    # Update an existing attachment by its ID
    attachment = Attachments.query.get(id)
    if not attachment:
        abort(404, 'Attachment not found')

    data = request.json
    name = data.get('name')
    type = data.get('type')

    # Validate the input
    if not name or not type:
        abort(400, 'Name and type are required')

    attachment.name = name
    attachment.type = type
    db.session.commit()

    return jsonify(attachment.as_dict())


@weapons.route('/weapon_attachments', methods=['POST'])
@token_required
def create_weapon_attachment():
    # Get the request data
    data = request.json

    # Extract the required fields
    weapon_id = data.get('weapon_id')
    attachment_id = data.get('attachment_id')
    attachment_type = data.get('attachment_type')

    # Validate the required fields
    if not weapon_id or not attachment_id or not attachment_type:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the weapon exists
    weapon = Weapons.query.get(weapon_id)
    if not weapon:
        return jsonify({'message': 'Weapon not found'}), 404

    # Check if the attachment exists
    attachment = Attachments.query.get(attachment_id)
    if not attachment:
        return jsonify({'message': 'Attachment not found'}), 404

    # Create a new WeaponAttachment instance
    weapon_attachment = WeaponAttachment(
        weapon_id=weapon_id,
        attachment_id=attachment_id,
        attachment_type=attachment_type
    )

    # Add the new WeaponAttachment to the database session
    db.session.add(weapon_attachment)
    db.session.commit()

    return jsonify({'message': 'WeaponAttachment created successfully', 'weapon_attachment': weapon_attachment.as_dict()}), 201