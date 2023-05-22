from urllib import request
from flask import Blueprint
from flask import request, jsonify, make_response, url_for, redirect, abort
from AC.database.models import Attachments, Tacticals, Users, WeaponAttachment, Weapons
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
        print(request.headers['Authorization'])
        # Check if Authorization header is present and extract token from it
        if 'Authorization' in request.headers:
            print(request.headers['Authorization'])
            token = request.headers['Authorization'].split(' ')[1]
            
        # Return 401 error if token is missing
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode token and get user ID
            data = jwt.decode(token, "MY_ENCODE_KEY", algorithms=['HS256'])
            current_user = Users.query.get(data['sub'])
        except:
            # Return 401 error if token is invalid
            return jsonify({'message': 'Token is invalid'}), 401

        # Call the route function with the current user as an argument
        return f(current_user, *args, **kwargs)

    return decorated


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = Users(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    token = user.encode_token()
    response = {
        'message': 'User registered successfully',
        'token': token,
        'email':data['email'],
        "name":data['name']
    }
    return jsonify(response), 201


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    user = Users.query.filter_by(email=data['email']).first()
    print(user.password_hash,data['password'],check_password_hash(user.password_hash, data['password']))
    if user and check_password_hash(user.password_hash, data['password']):
        token = user.encode_token()
        response = {
            'message': 'User logged in successfully',
            'token': token,
            'email':user.email,
            "name":user.name
        }
        return jsonify(response), 200
    else:
        response = {'message': 'Invalid email or password'}
        return jsonify(response), 401
    


@auth.route('/auth/facebook', methods=['POST'])
def facebook_login():
    data = request.get_json()
    print(data,"got it")
    facebook_data = data['facebook']
    user = Users.query.filter_by(facebook_id=facebook_data['id']).first()
    print(data,"got it",user)
    if user:
        token = user.encode_token()
        response = {
            'message': 'User logged in successfully with Facebook',
            'token': token,
            'email':user.email,
            "name":user.name
        }
        return jsonify(response), 200
    else:
        user = Users.query.filter_by(email=facebook_data['email']).first()
        if user:
            user.facebook_id = facebook_data['id']
            db.session.commit()
            token = user.encode_token()
            response = {
                'message': 'User registered and linked with Facebook',
                'token': token,
                'email':user.email,
                "name":user.name
            }
            return jsonify(response), 201
        else:
            user = Users(name=facebook_data['name'], email=facebook_data['email'],password=facebook_data['id'] ,facebook_id=facebook_data['id'])
            db.session.add(user)
            db.session.commit()
            token = user.encode_token()
            response = {
                'message': 'User registered and logged in successfully with Facebook',
                'token': token,
                'email':user.email,
                "name":user.name
            }
            return jsonify(response), 201
        
@auth.route('/auth/google', methods=['POST'])
def google_login():
    data = request.get_json()
    google_data = data.google
    
    # Check if the user exists based on the Google ID
    user = Users.query.filter_by(google_id=google_data['id']).first()
    if user:
        # If the user exists, generate a token and return a successful response
        token = user.encode_token()
        response = {
            'message': 'User logged in successfully with Google',
            'token': token,
            'email': user.email,
            'name': user.name
        }
        return jsonify(response), 200
    else:
        # If the user doesn't exist, check if there is a user with the same email
        user = Users.query.filter_by(email=google_data['email']).first()
        if user:
            # If a user with the same email exists, link the Google ID to the user and return a successful response
            user.google_id = google_data['id']
            db.session.commit()
            token = user.encode_token()
            response = {
                'message': 'User registered and linked with Google',
                'token': token,
                'email': user.email,
                'name': user.name
            }
            return jsonify(response), 201
        else:
            # If no user with the same email exists, create a new user with the Google data and return a successful response
            user = Users(name=google_data['name'], email=google_data['email'],password=google_data['id'] , google_id=google_data['id'])
            db.session.add(user)
            db.session.commit()
            token = user.encode_token()
            response = {
                'message': 'User registered and logged in successfully with Google',
                'token': token,
                'email': user.email,
                'name': user.name
            }
            return jsonify(response), 201


@auth.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')

    if not email or not old_password or not new_password:
        return jsonify({'error': 'Email, old password, and new password are required'}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Verify the old password
    if not user.check_password(old_password):
        return jsonify({'error': 'Invalid old password'}), 401

    # Update the user's password
    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password reset successful'})