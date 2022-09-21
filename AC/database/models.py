from enum import unique
from .. import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Field(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    create_date = db.Column(db.DateTime(timezone=True), default=func.now())
    devices = db.relationship('Device')

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.Integer, db.ForeignKey('field.id'))
    code = db.Column(db.String(8))
    type = db.Column(db.String(20))