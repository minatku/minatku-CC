from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import jwt_required
from .extensions import db, authorizations
from .models import User, MajorPredict
from .api_models import user_edit_model
from werkzeug.datastructures import FileStorage

# Namespace
ns_user = Namespace("User", description="buat proses usernya minatku", authorizations=authorizations)

# Endpoint for getting user by ID
@ns_user.route("/user/<int:user_id>")
class UserById(Resource):
    method_decorators = [jwt_required()]
    @ns_user.doc(security="jsonWebToken")
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            user_data = {
                "id_user": user.id_user,
                "email": user.email,
                "username": user.username,
                "nama_lengkap": user.nama_lengkap,
                "tanggal_lahir": user.tanggal_lahir.isoformat() if user.tanggal_lahir else None,
                "gender": user.gender,
                "no_telepon": user.no_telepon,
                "lokasi": user.lokasi,
                "is_premium": user.is_premium,
                "foto_profil": user.foto_profil,
                "create_at": user.create_at.isoformat() if user.create_at else None,
                "update_at": user.update_at.isoformat() if user.update_at else None,
                "major_predict": [],
            }
            # Fetch major_predict records for the current user
            major_predicts = MajorPredict.query.filter_by(id_user=user.id_user).all()
            # Populate major_predict data
            for major_predict in major_predicts:
                major_predict_data = {
                    "top_1": major_predict.top_1,
                    "top_2": major_predict.top_2,
                    "top_3": major_predict.top_3,
                    "top_4": major_predict.top_4,
                    "top_5": major_predict.top_5,
                    "create_at": major_predict.create_at.isoformat() if major_predict.create_at else None,
                    "update_at": major_predict.update_at.isoformat() if major_predict.update_at else None,
                }

                user_data["major_predict"].append(major_predict_data)

            return user_data, 200
        else:
            return {"message": "User not found"}, 404

    @ns_user.doc(security="jsonWebToken")
    @ns_user.expect(user_edit_model, validate=True)
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            # Update user information based on the received data
            # user.email = data.get("email", user.email)
            user.username = data.get("username", user.username)
            user.nama_lengkap = data.get("nama_lengkap", user.nama_lengkap)
            user.tanggal_lahir = data.get("tanggal_lahir", user.tanggal_lahir)
            user.gender = data.get("gender", user.gender)
            user.no_telepon = data.get("no_telepon", user.no_telepon)
            user.lokasi = data.get("lokasi", user.lokasi)
            db.session.commit()
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    @ns_user.doc(security="jsonWebToken")
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

@ns_user.route('/users')
class GetAllUsers(Resource):
    def get(self):
        users = User.query.all()
        users_data = []

        for user in users:
            user_data = {
                "id_user": user.id_user,
                "email": user.email,
                "username": user.username,
                "nama_lengkap": user.nama_lengkap,
                "tanggal_lahir": user.tanggal_lahir.isoformat() if user.tanggal_lahir else None,
                "gender": user.gender,
                "no_telepon": user.no_telepon,
                "lokasi": user.lokasi,
                "is_premium": user.is_premium,
                "foto_profil": user.foto_profil,
                "create_at": user.create_at.isoformat() if user.create_at else None,
                "update_at": user.update_at.isoformat() if user.update_at else None,
                "major_predict": [],
            }

            # Fetch major_predict records for the current user
            major_predicts = MajorPredict.query.filter_by(id_user=user.id_user).all()

            # Populate major_predict data
            for major_predict in major_predicts:
                major_predict_data = {
                    "top_1": major_predict.top_1,
                    "top_2": major_predict.top_2,
                    "top_3": major_predict.top_3,
                    "top_4": major_predict.top_4,
                    "top_5": major_predict.top_5,
                    "create_at": major_predict.create_at.isoformat() if major_predict.create_at else None,
                    "update_at": major_predict.update_at.isoformat() if major_predict.update_at else None,
                }

                user_data["major_predict"].append(major_predict_data)

            users_data.append(user_data)

        return users_data

# Add a parser for file upload
upload_parser = ns_user.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Profile picture file')

# Endpoint for uploading user profile picture
@ns_user.route("/user/<int:user_id>/profile-picture")
class UserProfilePicture(Resource):
    method_decorators = [jwt_required()]

    @ns_user.doc(security="jsonWebToken")
    @ns_user.expect(upload_parser)
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        args = upload_parser.parse_args()
        profile_picture = args['file']

        # Save the file to a folder (you need to create the folder if it doesn't exist)
        upload_folder = 'C:/Users/LENOVO/Downloads/minatku-api/static'
        file_path = f"{upload_folder}/{user_id}_profile_picture.jpg"
        profile_picture.save(file_path)

        # Update the user's profile picture path in the database
        user.foto_profil = file_path
        db.session.commit()

        return {"message": "Profile picture uploaded successfully"}, 200

    @ns_user.doc(security="jsonWebToken")
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        # Return the path to the user's profile picture
        return {"profile_picture": user.foto_profil}, 200

