from flask import Flask
from flask_cors import CORS
from .extensions import api, db, jwt
from .user import ns_user, UserProfilePicture
from .pertanyaan import ns_pertanyaan
from .auth import ns_auth
from .major import ns_predict
from .models import User
import os

def create_app():
    app = Flask(__name__)

    # Cloud SQL database configuration
    db_user = "your_user_name"
    db_password = "your_db_password"
    db_name = "your_db_name"
    db_host = "your_db_host"  # Ganti dengan alamat IP publik database
    db_port = 3306
    db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    
    CORS(app)
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    api.add_namespace(ns_user)
    api.add_namespace(ns_pertanyaan)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_predict)
    api.add_resource(UserProfilePicture, '/minatku/user/<int:user_id>/profile-picture')

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(email=identity).first()

    return app
