from flask import Flask
from os import path
from flask_migrate import Migrate
import json
from flask_cors import CORS
from .db import db


migrate = Migrate()

DB_NAME = 'AC.db'


def create_app():
    app = Flask(__name__)
    # secret hash key
    app.config['SECRET_KEY'] = 'KekronMekron-Hask-Key'

    # init db 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:letmein123@ac-dev.cl2yr0yt9ms9.us-west-1.rds.amazonaws.com:5432/postgres'
    db.init_app(app)
    migrate.init_app(app,db)
    
    #CORS
    CORS(app)

    #check if this is used
    
    

    # import all routes
    from .routes.views import views
    from .routes.auth import auth
    # url_prefix can add a prefix to the url
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')



    create_database(app)

    return app


def create_database(app):
    # if not path.exists('AC/' + DB_NAME):
    with app.app_context():
        db.create_all(app=app)
    print('NEW Database Created')