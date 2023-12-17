from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import jwt_required, current_user
from .extensions import db, authorizations
from .models import User, MajorPredict
from .api_models import user_edit_model
from werkzeug.datastructures import FileStorage
import os
from google.cloud import storage
import io
import uuid

# # Get the current file's directory
# current_file_directory = os.path.dirname(__file__)

# # Construct the absolute path to the credentials file
# credentials_path = os.path.join(current_file_directory, "minatku-8f0163a46a4c.json")
# print("Absolute path to credentials file:", credentials_path)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "minatku-2773c5450672.json"

# Namespace
ns_user = Namespace("User", description="buat proses usernya minatku", authorizations=authorizations)

# Add a parser for file upload
upload_parser = ns_user.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Profile picture file')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # Add more image formats as needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint for uploading user profile picture
@ns_user.route("/user/<int:user_id>/profile-picture")
class UserProfilePicture(Resource):
    method_decorators = [jwt_required()]

    @ns_user.doc(security="jsonWebToken")
    @ns_user.expect(upload_parser)
    def post(self, user_id):
        if current_user.id_user != user_id and current_user.is_admin == False:
            return {"error": "Unauthorized access to user data"}, 403
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        args = upload_parser.parse_args()
        profile_picture = args['file']

        # Check if the file format is allowed
        if not allowed_file(profile_picture.filename):
            return {"error": "Invalid file format. Only jpg, jpeg, png, and gif are allowed."}, 400

        # Generate a random filename using uuid
        random_filename = str(uuid.uuid4())
        file_extension = profile_picture.filename.rsplit('.', 1)[1].lower()
        random_filename_with_extension = f"{random_filename}.{file_extension}"

        # Upload to Google Cloud Storage with the random filename
        bucket_name = 'minatku_bucket'
        blob = storage.Client().bucket(bucket_name).blob(random_filename_with_extension)
        blob.upload_from_file(io.BytesIO(profile_picture.read()), content_type=profile_picture.content_type)

        # Get the uploaded file URL
        file_url = blob.public_url

        # Update the profile picture link in the database
        user.foto_profil = file_url
        db.session.commit()

        return {"message": "Profile picture uploaded successfully", "file_url": file_url}, 200

    @ns_user.doc(security="jsonWebToken")
    def get(self, user_id):
        if current_user.id_user != user_id and current_user.is_admin == False:
            return {"error": "Unauthorized access to user data"}, 403
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        # Return the URL to the user's profile picture
        return {"profile_picture": user.foto_profil}, 200

# Endpoint for getting user by ID
@ns_user.route("/user/<int:user_id>")
class UserById(Resource):
    method_decorators = [jwt_required()]
    @ns_user.doc(security="jsonWebToken")
    def get(self, user_id):
        if current_user.id_user != user_id and current_user.is_admin ==False:
            return {"error": "Unauthorized access to user data"}, 403
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
        if current_user.id_user != user_id and current_user.is_admin ==False:
            return {"error": "Unauthorized access to user data"}, 403
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
        if current_user.id_user != user_id and current_user.is_admin ==False:
            return {"error": "Unauthorized access to user data"}, 403
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

@ns_user.route('/users')
class GetAllUsers(Resource):
    method_decorators = [jwt_required()]

    @ns_user.doc(security="jsonWebToken")
    def get(self):
        if current_user.is_admin ==False:
            return {"error": "Unauthorized access to user data"}, 403
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
