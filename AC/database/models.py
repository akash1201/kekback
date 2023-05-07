from enum import unique
from ..db import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Identity, DateTime
from datetime import datetime, timedelta
import json
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSONB
from werkzeug.security import generate_password_hash, check_password_hash
import jwt



# User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    facebook_id = db.Column(db.String(50), unique=True)
    google_id = db.Column(db.String(50), unique=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_token(self):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': self.id
        }
        key = jwt.encode(
            payload,
            "MY_ENCODE_KEY", #need to make this secure
            algorithm='HS256'
        ) 
        return key

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, "MY_ENCODE_KEY")
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    




class Attachments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    weapons = db.relationship("WeaponAttachment", back_populates="attachment")
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Weapons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    subType = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    ammo = db.Column(db.String(20))
    modelUrl = db.Column(db.String(50))
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)

    attachments = db.relationship("WeaponAttachment", back_populates="weapon")
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class WeaponAttachment(db.Model):
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapons.id'), primary_key=True)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.id'), primary_key=True)
    attachment_type = db.Column(db.String(20), nullable=False)

    weapon = db.relationship("Weapons", back_populates="attachments")
    attachment = db.relationship("Attachments", back_populates="weapons")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}







class Tacticals(db.Model):
    id = db.Column(db.Integer, Identity(start=1),primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    trigger = db.Column(db.String(20), nullable=False)
    ammo = db.Column(db.String(20))
    modelUrl = db.Column(db.String(20))
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
