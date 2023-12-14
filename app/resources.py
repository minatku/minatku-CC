from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import *
from .api_models import *
from flask import jsonify
import numpy as np
from sklearn.preprocessing import normalize
from keras.models import load_model
from datetime import datetime

classes = ['Science', 'Arts and Literature', 'Economics', 'Technology', 'Social']
authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
# Namespace
ns = Namespace("Minatku", description="Cihuyyy", authorizations=authorizations)

model = load_model('app/model.h5', compile=False)

print('Model loaded. Start serving...')

@ns.route("/predict")
class PredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    @ns.expect(input_predict_model, validate=True)
    def post(self):
        data = request.get_json()
        input_data = data["input"]

        # Ensure input_data is a 2D array
        input_data = np.array(input_data).reshape(1, -1)

        # Normalize the input data
        fitur_normalized = normalize(input_data, axis=0)

        # Make predictions using the model
        prediction = model.predict(fitur_normalized)
        sorted_indices = np.argsort(-prediction[0])
        sorted_classes = [classes[idx] for idx in sorted_indices]
        sorted_indices = sorted_indices.tolist()

        # Format the prediction results to be returned to the client
        result = {
            "prediction_class": sorted_indices[0],
            "prediction_label": classes[sorted_indices[0]],
            "all_prediction_class": sorted_indices,
            "all_prediction_labels": sorted_classes,
        }
        save_to_database(result)
        return jsonify(result)
def save_to_database(prediction_result):
    # Create a new MajorPredict entry
    major_predict_entry = MajorPredict(
        top_1=classes[prediction_result["all_prediction_class"][0]],
        top_2=classes[prediction_result["all_prediction_class"][1]],
        top_3=classes[prediction_result["all_prediction_class"][2]],
        top_4=classes[prediction_result["all_prediction_class"][3]],
        top_5=classes[prediction_result["all_prediction_class"][4]],
        id_user=current_user.id_user,
        create_at=datetime.now()
    )

    # Add and commit the new entry to the database
    db.session.add(major_predict_entry)
    db.session.commit()

# Endpoint for user registration
@ns.route("/register")
class Register(Resource):
    @ns.expect(user_registration_model, validate=True)
    def post(self):
        data = request.get_json()

        # Check if the email is already registered
        existing_email_user = User.query.filter_by(email=data["email"]).first()
        if existing_email_user:
            return {"message": "Email already registered. Please use a different email."}, 400

        # Check if the username is already registered
        existing_username_user = User.query.filter_by(username=data["username"]).first()
        if existing_username_user:
            return {"message": "Username already registered. Please choose a different username."}, 400

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
        return {"message": "User registered successfully"}, 201

@ns.route("/login")
class Login(Resource):

    @ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(email=ns.payload["email"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password, ns.payload["password"]):
            return {"error": "Incorrect password"}, 401
        create_access_token(user.email)
        return {"access_token": create_access_token(user.email)}
    
@ns.route("/whoami")
class WhoAmI(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    def get(self):
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
            "foto_profil": current_user.foto_profil,
            "create_at": current_user.create_at.isoformat() if current_user.create_at else None,
            "update_at": current_user.update_at.isoformat() if current_user.update_at else None,
        }
        return jsonify({
            "message": "Data user yang sedang login",
            "user_details": user_details,
        })


@ns.route("/major_predict/<int:user_id>")
class MajorPredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    def get(self, user_id):
        # Check if the current user has the permission to access major predict data
        if current_user.id_user != user_id:
            return {"error": "Unauthorized access to major predict data"}, 403

        # Query major predict data for the specified user ID
        major_predict_data = MajorPredict.query.filter_by(id_user=user_id).first()

        if major_predict_data:
            # Format the major predict results to be returned to the client
            result = {
                "id_major_predict": major_predict_data.id_major_predict,
                "top_1": major_predict_data.top_1,
                "top_2": major_predict_data.top_2,
                "top_3": major_predict_data.top_3,
                "top_4": major_predict_data.top_4,
                "top_5": major_predict_data.top_5,
                "id_user":major_predict_data.id_user,
                "create_at":major_predict_data.create_at,
                "update_at":major_predict_data.update_at
            }
            return jsonify(result)
        else:
            return {"message": "Major predict data not found for the specified user"}, 404
        
# Endpoint for getting user by ID
@ns.route("/user/<int:user_id>")
class UserById(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
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

    @ns.doc(security="jsonWebToken")
    @ns.expect(user_edit_model, validate=True)
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            # Update user information based on the received data
            user.email = data.get("email", user.email)
            user.username = data.get("username", user.username)
            user.nama_lengkap = data.get("nama_lengkap", user.nama_lengkap)
            user.tanggal_lahir = data.get("tanggal_lahir", user.tanggal_lahir)
            user.gender = data.get("gender", user.gender)
            user.no_telepon = data.get("no_telepon", user.no_telepon)
            user.lokasi = data.get("lokasi", user.lokasi)
            user.is_premium = data.get("is_premium", user.is_premium)
            user.foto_profil = data.get("foto_profil", user.foto_profil)
            db.session.commit()
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    @ns.doc(security="jsonWebToken")
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

# Endpoint for getting all users
@ns.route('/users')
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
                "create_at":user.create_at,
                "update_at":user.update_at,
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

# Menambahkan endpoint pertanyaan ke dalam namespace yang sudah ada
@ns.route("/pertanyaan")
class PertanyaanResource(Resource):
    @ns.expect(pertanyaan_model, validate=True)
    def post(self):
        data = request.get_json()
        new_pertanyaan = Pertanyaan(
            isi_pertanyaan=data["isi_pertanyaan"],
            kode=data["kode"],
            kelas_pertanyaan=data["kelas_pertanyaan"],
        )
        db.session.add(new_pertanyaan)
        db.session.commit()
        return {"message": "Pertanyaan created successfully"}, 201

    def get(self):
        pertanyaan = Pertanyaan.query.all()
        pertanyaan_data = [
            {
                "id_pertanyaan": p.id_pertanyaan,
                "isi_pertanyaan": p.isi_pertanyaan,
                "kode": p.kode,
                "kelas_pertanyaan": p.kelas_pertanyaan,
            }
            for p in pertanyaan
        ]
        return pertanyaan_data
    
@ns.route("/pertanyaan/<int:id_pertanyaan>")
class PertanyaanByIdResource(Resource):
    def get(self, id_pertanyaan):
        pertanyaan = Pertanyaan.query.get(id_pertanyaan)
        if pertanyaan:
            pertanyaan_data = {
                "id_pertanyaan": pertanyaan.id_pertanyaan,
                "isi_pertanyaan": pertanyaan.isi_pertanyaan,
                "kode": pertanyaan.kode,
                "kelas_pertanyaan": pertanyaan.kelas_pertanyaan,
            }
            return pertanyaan_data, 200
        else:
            return {"message": "Pertanyaan not found"}, 404

    def put(self, id_pertanyaan):
        pertanyaan = Pertanyaan.query.get(id_pertanyaan)
        if pertanyaan:
            data = request.get_json()
            # Update pertanyaan information based on the received data
            pertanyaan.isi_pertanyaan = data.get("isi_pertanyaan", pertanyaan.isi_pertanyaan)
            pertanyaan.kode = data.get("kode", pertanyaan.kode)
            pertanyaan.kelas_pertanyaan = data.get("kelas_pertanyaan", pertanyaan.kelas_pertanyaan)
            db.session.commit()
            return {"message": "Pertanyaan updated successfully"}, 200
        else:
            return {"message": "Pertanyaan not found"}, 404

    def delete(self, id_pertanyaan):
        pertanyaan = Pertanyaan.query.get(id_pertanyaan)
        if pertanyaan:
            db.session.delete(pertanyaan)
            db.session.commit()
            return {"message": "Pertanyaan deleted successfully"}, 200
        else:
            return {"message": "Pertanyaan not found"}, 404

