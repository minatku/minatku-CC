from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import *
from .api_models import *
from flask import jsonify
import numpy as np
from sklearn.preprocessing import normalize
import tensorflow as tf
from keras.models import load_model

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
    @ns.expect(predict_model, validate=True)
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
        return jsonify(result)


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
    

# Endpoint for getting all users
@ns.route('/users')
class GetAllUsers(Resource):
    def get(self):
        users = User.query.all()
        users_data = [
            {
                "id_user": user.id_user,
                "email": user.email,
                "username": user.username,
                "nama_lengkap": user.nama_lengkap,
                "tanggal_lahir": user.tanggal_lahir.isoformat() if user.tanggal_lahir else None,
                "gender": user.gender,
                "no_telepon": user.no_telepon,
                "lokasi": user.lokasi,
                "is_premium": user.is_premium,
                "id_major": user.id_major,
                "foto_profil": user.foto_profil,
            }
            for user in users
        ]
        return users_data

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
                "id_major": user.id_major,
                "foto_profil": user.foto_profil,
            }
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
            user.id_major = data.get("id_major", user.id_major)
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

