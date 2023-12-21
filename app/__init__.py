from flask import Flask
from flask_cors import CORS
from .extensions import api, db, jwt
from .user import ns_user, UserProfilePicture
from .pertanyaan import ns_pertanyaan
from .auth import ns_auth
from .major import ns_predict
from .models import User
from google.cloud import secretmanager

def fetch_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/minatku/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=secret_path)
    return response.payload.data.decode('UTF-8')

def create_app():
    app = Flask(__name__)

    # Fetch database credentials from Secret Manager
    db_user = fetch_secret("db-credentials")["db_user"]
    db_password = fetch_secret("db-credentials")["db_password"]
    db_name = fetch_secret("db-credentials")["db_name"]
    db_host = fetch_secret("db-credentials")["db_host"]
    db_port = fetch_secret("db-credentials")["db_port"]

    # Fetch JWT secret key from Secret Manager
    jwt_secret_key = fetch_secret("jwt-secret-key")["jwt_secret_key"]

    # Configure the connection string
    db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["JWT_SECRET_KEY"] = jwt_secret_key
    # Set the expiration time for the access token to 1 hour (3600 seconds)
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
