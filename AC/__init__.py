from flask import Flask
from os import path
# from flask_migrate import Migrate
import json
from flask_cors import CORS

from sqlalchemy.dialects.postgresql import insert
from AC.database.models import Attachments, WeaponAttachment, Weapons
from .db import db

from .baseData.mock import guns, attachments, weaponAttachment

# migrate = Migrate()

DB_NAME = 'AC.db'


def create_app():
    app = Flask(__name__)
    # secret hash key
    app.config['SECRET_KEY'] = 'KekronMekron-Hask-Key'

    # init db 
    # 'postgresql://postgres:ranju12@localhost/postgres' #
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:letmein123@awseb-e-fktk82fxnm-stack-awsebrdsdatabase-8pykg4ugzxha.cl2yr0yt9ms9.us-west-1.rds.amazonaws.com:5432/ebdb'
    db.init_app(app)
    # migrate.init_app(app,db)
    
    #CORS
    CORS(app)

    # import all routes
    from .routes.views import views
    from .routes.auth import auth
    from .routes.weapons import weapons
    from .routes.tacticals import tacticals
    from .routes.users import users
    # url_prefix can add a prefix to the url
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(weapons,url_prefix='/')
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
