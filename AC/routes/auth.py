from urllib import request
from flask import Blueprint
from flask import request, jsonify, make_response, url_for, redirect, abort
from AC.database.models import Attachments, Tacticals, User, WeaponAttachment, Weapons
from .. import db
from functools import wraps
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
auth = Blueprint('auth', __name__)

# Decorator to check if user is logged in
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(" we got here")
        # Check if Authorization header is present and extract token from it
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        # Return 401 error if token is missing
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Decode token and get user ID
            data = jwt.decode(token, "MY_ENCODE_KEY", algorithms=['HS256'])
            current_user = User.query.get(data['id'])
        except:
            # Return 401 error if token is invalid
            return jsonify({'message': 'Token is invalid'}), 401

        # Call the route function with the current user as an argument
        return f(current_user, *args, **kwargs)

    return decorated


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    password_hash = generate_password_hash(data['password'])
    user = User(name=data['name'], email=data['email'], password=password_hash)
    db.session.add(user)
    db.session.commit()
    token = user.encode_token()
    response = {
        'message': 'User registered successfully',
        'token': token.decode('UTF-8')
    }
    return jsonify(response), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    user = User.query.filter_by(email=data['email']).first()
    if user and  check_password_hash(user.password_hash, data['password']):
        token = user.encode_token()
        response = {
            'message': 'User logged in successfully',
            'token': token
        }
        return jsonify(response), 200
    else:
        response = {'message': 'Invalid email or password'}
        return jsonify(response), 401
    


@auth.route('/auth/facebook', methods=['POST'])
def facebook_login():
    data = request.get_json()
    facebook_data = data.facebook
    user = User.query.filter_by(facebook_id=facebook_data['id']).first()
    if user:
        token = user.encode_token()
        response = {
            'message': 'User logged in successfully with Facebook',
            'token': token.decode('UTF-8')
        }
        return jsonify(response), 200
    else:
        user = User.query.filter_by(email=facebook_data['email']).first()
        if user:
            user.facebook_id = facebook_data['id']
            db.session.commit()
            token = user.encode_token()
            response = {
                'message': 'User registered and linked with Facebook',
                'token': token.decode('UTF-8')
            }
            return jsonify(response), 201
        else:
            user = User(name=facebook_data['name'], email=facebook_data['email'], facebook_id=facebook_data['id'])
            db.session.add(user)
            db.session.commit()
            token = user.encode_token()
            response = {
                'message': 'User registered and logged in successfully with Facebook',
                'token': token.decode('UTF-8')
            }
            return jsonify(response), 201