from flask import request
from flask_restx import Resource, Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .extensions import api, db
from .models import User

# Namespace
ns = Namespace("auth", description="Authentication")

# User model for request parsing
user_model = ns.model(
    "User",
    {
        "email": fields.String(required=True),
        "username": fields.String(required=True),
        "nama_lengkap": fields.String(required=True),
        "password": fields.String(required=True),
        "tanggal_lahir": fields.Date(required=True),
        "gender": fields.String(required=True),
        "no_telepon": fields.String(required=True),
        "lokasi": fields.String(required=True),
        "is_premium": fields.Boolean(required=True),
        "id_major": fields.Integer(required=True),
        "foto_profil": fields.String(required=True),
    },
)

# Endpoint for user registration
@ns.route("/register")
class Register(Resource):
    @ns.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(**data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201


# Endpoint for user login
@ns.route("/login")
class Login(Resource):
    @ns.expect(user_model, validate=True)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data["username"]).first()

        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id_user)
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401


# Endpoint for user logout
@ns.route("/logout")
class Logout(Resource):
    @jwt_required()
    def post(self):
        return {"message": "User logged out successfully"}, 200


# Endpoint for getting user data
@ns.route("/user")
class GetUserData(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            user_data = {
                "id_user": user.id_user,
                "email": user.email,
                "username": user.username,
                "nama_lengkap": user.nama_lengkap,
                "tanggal_lahir": user.tanggal_lahir.isoformat(),
                "gender": user.gender,
                "no_telepon": user.no_telepon,
                "lokasi": user.lokasi,
                "is_premium": user.is_premium,
                "id_major": user.id_major,
                "foto_profil": user.foto_profil,
            }
            return user_data, 200
        else:
            return {"message": "User not found"}, 404
