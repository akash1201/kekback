from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

DB_NAME = 'AC.db'


def create_app():
    app = Flask(__name__)
    # secret hash key
    app.config['SECRET_KEY'] = 'KekronMekron-Hask-Key'

    # init db Start
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:letmein123@ac-dev.cl2yr0yt9ms9.us-west-1.rds.amazonaws.com:5432/AC-dev'
    db.init_app(app)
    # init db End

    # import all routes
    from .routes.views import views
    from .routes.auth import auth
    # url_prefix can add a prefix to the url
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    create_database(app)
    from .database.models import Users

    return app


def create_database(app):
    if not path.exists('AC/' + DB_NAME):
        db.create_all(app=app)
        print('NEW Database Created')