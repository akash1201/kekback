from flask import Flask
from os import path
# from flask_migrate import Migrate
import json
from flask_cors import CORS
from enum import Enum
from sqlalchemy.dialects.postgresql import insert
from AC.database.models import Attachments, WeaponAttachment, Weapons
from .db import db
from datetime import datetime
from .baseData.mock import guns, attachments, weaponAttachment

# migrate = Migrate()

DB_NAME = 'AC.db'


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def create_app(env):
    app = Flask(__name__)
    # secret hash key
    app.config['SECRET_KEY'] = 'KekronMekron-Hask-Key'

    #define custom json encoder for json package so it knows our custom enums
    app.json_encoder = MyJSONEncoder

    # init db 
    # 'postgresql://postgres:ranju12@localhost/postgres' #
    print(env, "env app is launched with")
    if env == '1':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:letmein123@localhost:5432/postgres'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:letmein123@54.151.55.87:5432/dev'






    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:letmein123@54.151.55.87:5432/dev'
    db.init_app(app)
    # migrate.init_app(app,db)
    
    #CORS
    CORS(app)

    # import all routes
    from .routes.views import views
    from .routes.auth import auth
    from .routes.weapons import weapons
    from .routes.characters import characters
    from .routes.tacticals import tacticals
    from .routes.users import users
    # url_prefix can add a prefix to the url
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(weapons,url_prefix='/')
    app.register_blueprint(characters,url_prefix='/')
    app.register_blueprint(tacticals,url_prefix='/')
    app.register_blueprint(users,url_prefix='/')

    create_database(app)

    # create_data(db)
    

    return app


def create_database(app):
    app.app_context().push()
    db.create_all(app=app)
    print('NEW Database Created')


def create_data(db):
    for gun in guns:
        weapon = Weapons.query.filter_by(id=gun['id']).first()
        if weapon is None:
            new_weapon = Weapons(**gun)
            db.session.add(new_weapon)
    db.session.commit()

    for attachment in attachments:
        attachmentExists = Attachments.query.filter_by(id=attachment['id']).first()
        if attachmentExists is None:
            new_attachment = Attachments(**attachment)
            db.session.add(new_attachment)
    db.session.commit()

    for wa in weaponAttachment:
        attachmentExists = WeaponAttachment.query.filter_by(weapon_id=wa['weapon_id'], attachment_id=wa['attachment_id'] ).first()
        if attachmentExists is None:
            new_attachment = WeaponAttachment(**wa)
            db.session.add(new_attachment)
    db.session.commit()
