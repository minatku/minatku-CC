from flask import Flask 

from .extensions import api, db, jwt
from .resources import ns

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/minatku"
    app.config["JWT_SECRET_KEY"] = "thisisasecret"
  
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    api.add_namespace(ns)

    return app