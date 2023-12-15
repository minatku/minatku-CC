from flask_sqlalchemy import SQLAlchemy 
from flask_restx import Api
from flask_jwt_extended import JWTManager
from keras.models import load_model
api = Api()
db = SQLAlchemy()
jwt = JWTManager()
authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
model = load_model('app/model.h5', compile=False)

print('Model loaded. Start serving...')