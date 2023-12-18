from flask import Flask 
from flask_cors import CORS
from .extensions import api, db, jwt
from .user import ns_user, UserProfilePicture
from .pertanyaan import ns_pertanyaan
from .auth import ns_auth
from .major import ns_predict
from .models import User

def create_app():
    app = Flask(__name__)

    # Cloud SQL database configuration
    db_user = "root"
    db_password = "minatku1234567"
    db_name = "db_minatku"
    db_socket_dir = "/cloudsql"
    cloud_sql_connection_name = "minatku:asia-southeast2:dbminatku"
    db_host = "34.101.48.255"  # Ganti dengan alamat IP publik database
    db_port = 3306

    # Configure the connection string
    db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["JWT_SECRET_KEY"] = "thisisasecret"

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
