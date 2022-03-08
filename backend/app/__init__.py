from flask import Flask 
from flask_restx import Api
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from app.config import config




def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
   
    @app.shell_context_processor
    def make_shell_context():
        return{
            "db": db,
            "User": User
        }
       
    return app

def init_db_app(db,app):
    db.init_app(app)
    print('Database initiated!') 
    
def create_database(db,app):
    db.create_all(app=app)
    print('created database!') 


config_name = os.getenv('FLASK_CONFIG')
myapp = create_app(config_name)

db = SQLAlchemy(myapp)
init_db_app(db, myapp)
create_database(db,myapp)

login_manager = LoginManager()
login_manager.init_app(myapp)
login_manager.login_view = 'login'

migrate = Migrate(myapp, db)
migrate.init_app(myapp, db)


from app.user.auth import auth_ns
from app.user.admin import admin_ns
from app.tshirt.tshirtapi import tshirt_ns
from app.tshirt.orders import order_tshirt_ns
from app.tshirt.customers import customer_ns
from app.file.upload import upload_ns
from app.album.album import album_ns
from app.album.uploadsong import song_ns 

api = Api(myapp, doc='/docs') 
api.add_namespace(auth_ns)
api.add_namespace(admin_ns)
api.add_namespace(tshirt_ns)
api.add_namespace(order_tshirt_ns)
api.add_namespace(customer_ns)
api.add_namespace(upload_ns)
api.add_namespace(album_ns)
api.add_namespace(song_ns)


# from app.user.api import user_api
from app.user.models import User



@login_manager.user_loader
def load_user(users_id):
   return User.query.get(int(users_id))




    
    