from flask import Flask 

from .extensions import api, db, jwt
from .user import ns_user,UserProfilePicture
from .pertanyaan import ns_pertanyaan
from .auth import ns_auth
from .major import ns_predict
from .models import User
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/db_minatku"
    app.config["JWT_SECRET_KEY"] = "thisisasecret"
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