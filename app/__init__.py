from flask import Flask
from flask_cors import CORS
from .extensions import api, db, jwt
from .user import ns_user, UserProfilePicture
from .pertanyaan import ns_pertanyaan
from .auth import ns_auth
from .major import ns_predict
from .models import User
import json

def get_secret_from_json(json_file):
    with open(json_file, 'r') as file:
        secret_data = json.load(file)
    return secret_data

def create_app():
    app = Flask(__name__)

     # Cloud SQL database configuration
    # Cloud SQL database configuration
    db_user = "root"
    db_password = "minatku1234567"
    db_name = "db_minatku"
    db_socket_dir = "/cloudsql"
    cloud_sql_connection_name = "minatku:asia-southeast2:dbminatku"
    db_host = "34.101.48.255"  # Ganti dengan alamat IP publik database
    db_port = 3306

    # JWT configuration
    jwt_secret_key = get_secret_from_json("jwt-secret-key.json")
    app.config["JWT_SECRET_KEY"] = jwt_secret_key["jwt_secret_key"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

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

