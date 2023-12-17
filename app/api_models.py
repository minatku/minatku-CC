from flask_restx import fields

from .extensions import api 

input_predict_model = api.model('PredictModel', {
    'input': fields.List(fields.Integer, required=True, description='List of integers representing the feature vector'),
})

# Model for Major Predict
major_predict_model = api.model(
    "MajorPredict",
    {
        "id_major_predict": fields.Integer,
        "top_1": fields.String(required=True),
        "top_2": fields.String(required=True),
        "top_3": fields.String(required=True),
        "top_4": fields.String(required=True),
        "top_5": fields.String(required=True),
        "id_user":fields.String(required=True),
        "create_at": fields.DateTime,
        "update_at": fields.DateTime,
    },
)

# User model for request parsing
user_model = api.model(
    "User",
    {
        "id_user": fields.Integer(required=True),
        "email": fields.String(required=True),
        "username": fields.String(required=True),
        "nama_lengkap": fields.String(required=True),
        "password": fields.String(required=True),
        "tanggal_lahir": fields.Date(required=True),
        "gender": fields.String(required=True),
        "no_telepon": fields.String(required=True),
        "lokasi": fields.String(required=True),
        "is_premium": fields.Boolean(required=True),
        "foto_profil": fields.String(required=True),
        "create_at": fields.DateTime,
        "update_at": fields.DateTime,
    },
)

user_registration_model = api.model(
    "UserRegistration",
    {
        "email": fields.String(required=True),
        "username": fields.String(required=True),
        "nama_lengkap": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

login_model = api.model("LoginModel", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

# User model for request parsing
user_edit_model = api.model(
    "UserEdit",
    {
        "username": fields.String,
        "nama_lengkap": fields.String,
        "tanggal_lahir": fields.Date,
        "gender": fields.String,
        "no_telepon": fields.String,
        "lokasi": fields.String,
    },
)

# Model for pertanyaan
pertanyaan_model = api.model(
    "Pertanyaan",
    {
        "isi_pertanyaan": fields.String(required=True),
        "kode": fields.String(required=True),
        "kelas_pertanyaan": fields.String(required=True),
    },
)
pertanyaan_edit_model = api.model(
    "PertanyaanEdit",
    {
        "isi_pertanyaan": fields.String,
        "kode": fields.String,
        "kelas_pertanyaan": fields.String,
    },
)
