from flask_restx import Resource, Namespace
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt_identity, create_refresh_token
from .extensions import authorizations, db
from .models import User
from .api_models import user_registration_model, login_model
from datetime import datetime
from http import HTTPStatus
# Namespace
ns_auth = Namespace("Auth", description="buat autentikasi", authorizations=authorizations)


# Endpoint for Hello World
@ns_auth.route("/hello-world")
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello, CICD sukses!horeeee"}
    
@ns_auth.route("/register")
class Register(Resource):
    @ns_auth.expect(user_registration_model, validate=True)
    def post(self):
        data = request.get_json()

        # Check if the email is already registered
        existing_email_user = User.query.filter_by(email=data["email"]).first()
        if existing_email_user:
            return {"error": True, "message": "Email already registered. Please use a different email."}, 400

        # Check if the username is already registered
        existing_username_user = User.query.filter_by(username=data["username"]).first()
        if existing_username_user:
            return {"error": True, "message": "Username already registered. Please choose a different username."}, 400

        # If neither email nor username is already registered, proceed with registration
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(
            email=data["email"],
            username=data["username"],
            nama_lengkap=data["nama_lengkap"],
            password=hashed_password,
            create_at=datetime.now(),
        )
        db.session.add(new_user)
        db.session.commit()
        return {"error": False, "message": "User registered successfully"}, 201

@ns_auth.route("/login")
class Login(Resource):

    @ns_auth.expect(login_model)
    def post(self):
        user = User.query.filter_by(email=ns_auth.payload["email"]).first()
        if not user:
            return {"error": True, "message": "User does not exist", "loginResult": {}}, 401
        if not check_password_hash(user.password, ns_auth.payload["password"]):
            return {"error": True, "message": "Incorrect password", "loginResult": {}}, 401

        # Assuming you are using Flask-JWT-Extended for token creation
        access_token = create_access_token(user.email)
        refresh_token = create_refresh_token(identity=user.email)

        response_data = {
            "error": False,
            "message": "success",
            "loginResult": {
                "userId": user.id_user,
                "username": user.username,
                "email": user.email,
                "accessToken": access_token,
                "refreshToken": refresh_token
            }
        }

        return response_data
        
@ns_auth.route("/whoami")
class WhoAmI(Resource):
    method_decorators = [jwt_required()]

    @ns_auth.doc(security="jsonWebToken")
    def get(self):
        try:
            user_details = {
                "id_user": current_user.id_user,
                "email": current_user.email,
                "username": current_user.username,
                "nama_lengkap": current_user.nama_lengkap,
                "tanggal_lahir": current_user.tanggal_lahir.isoformat() if current_user.tanggal_lahir else None,
                "gender": current_user.gender,
                "no_telepon": current_user.no_telepon,
                "lokasi": current_user.lokasi,
                "is_premium": current_user.is_premium,
                "is_admin": current_user.is_admin,
                "foto_profil": current_user.foto_profil,
                "create_at": current_user.create_at.isoformat() if current_user.create_at else None,
                "update_at": current_user.update_at.isoformat() if current_user.update_at else None,
            }

            return {
                "error": False,
                "message": "Data user yang sedang login",
                "user_details": user_details,
            }
        except Exception as e:
            # Handle any exceptions and return an error message
            return {
                "error": True,
                "message": f"An error occurred: {str(e)}",
                "user_details": None,
            }

@ns_auth.route('/refresh')
class Refresh(Resource):
    method_decorators = [jwt_required()]

    @ns_auth.doc(security="jsonWebToken")
    def post(self):
        try:
            username = get_jwt_identity()
            access_token = create_access_token(identity=username)

            return {'error': False, 'message': 'Token refreshed successfully', 'access_token': access_token}, HTTPStatus.OK
        except Exception as e:
            # Handle any exceptions and return an error message
            return {'error': True, 'message': f'An error occurred: {str(e)}', 'access_token': None}, HTTPStatus.INTERNAL_SERVER_ERROR
