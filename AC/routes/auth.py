from urllib import request
from flask import Blueprint
from flask import jsonify, request, abort, make_response
from AC.database.models import Users, Weapons
from .. import db
import json
auth = Blueprint('auth', __name__)


@auth.route('/users', methods=['GET', 'POST'])
def home():
    items = Users.query.all()
    print(items)
    return jsonify(tems=items)






@auth.route('/weapons', methods=['GET'])
def getWeapons():
        items = Weapons.query.all()
        print(items)
        wepons = []
        for item in items:
            wepons.append(item.as_dict())
        return jsonify(wepons)

@auth.route('/weapons', methods=['POST'])
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
    

