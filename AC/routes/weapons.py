from urllib import request
from flask import Blueprint
from flask import jsonify, request, abort, make_response
from AC.database.models import Attachments, WeaponAttachment, Weapons
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
def newWeapon():
    if not request.json:
        abort(400)
    book = Weapons(
        name=request.json.get('name'),
        category=request.json.get('category'),
        type=request.json.get('type'),
        subType=request.json.get('subType'),
        action=request.json.get('action'),
        ammo=request.json.get('ammo'),
        modelUrl=request.json.get('modelUrl')
    )
    db.session.add(book) 
    db.session.commit()
    return jsonify(book.as_dict()), 201


@weapons.route('/weapon/<int:weapon_id>', methods=['DELETE'])
@token_required
def removeWeapon(weapon_id):
    weapon = Weapons.query.get(weapon_id)

    if not weapon:
        return jsonify({'error': f'weapon with id {weapon_id} does not exist'})

    WeaponAttachment.query.filter_by(weapon_id=weapon.id).delete()
    db.session.delete(weapon)
    db.session.commit()

    return jsonify({'message': f'weapon with id {weapon_id} and associated weapon attachments have been deleted'})


