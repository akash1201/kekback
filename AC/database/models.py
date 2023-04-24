from enum import unique
from ..db import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Identity, DateTime
from datetime import datetime 
import json
from sqlalchemy import event


class Users(db.Model):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Weapons(db.Model):
    id = db.Column(db.Integer, Identity(start=1),primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    subType = db.Column(db.String(20), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    ammo = db.Column(db.String(20))
    modelUrl = db.Column(db.String(50))
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)

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
