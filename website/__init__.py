# __init__.py : to make "website" as a library
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()  # define database

basedir = os.path.abspath(os.path.dirname(__file__))

DB_NAME = "sqlite_database.db"  # name of database


def create_app():
    app = Flask(__name__)   # __name__ represent the name of the file
    app.config['SECRET_KEY'] = 'dd'   # encrpt
    # my SQL db is store/located at this locattion
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialize db, tell the db that this is the app will gonna wse with db
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    '''
    url_prefix:
    all of the url that is store inside the blueprint how
    do I access them.
    For Ex:
    if app.register_blueprint(views, url_prefix="/views")
    now if I want to access to the views url I need to go
    /views/url ... for EX: /views/settings
    but if just app.register_blueprint(views, url_prefix="/")
    to access them jsut go to /settings
    '''

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    # where flask direct us if not loged in (login page)
    login_manager.login_view = 'auth.login'
    # telling login_manager which app we gonna use
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists(f'website/{DB_NAME}'):
        db.create_all(app=app)
        print('Created Batabase!')
