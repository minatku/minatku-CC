from flask_restx import fields

from .extensions import api 

# Assuming you have a feature named 'input' for prediction
predict_model = api.model('PredictModel', {
    'input': fields.List(fields.Integer, required=True, description='List of integers representing the feature vector'),
})

# User model for request parsing
user_model = api.model(
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
    "email": fields.String,
    "password": fields.String
})

# User model for request parsing
user_edit_model = api.model(
    "UserEdit",
    {
        "email": fields.String,
        "username": fields.String,
        "nama_lengkap": fields.String,
        "tanggal_lahir": fields.Date,
        "gender": fields.String,
        "no_telepon": fields.String,
        "lokasi": fields.String,
        "is_premium": fields.Boolean,
        "id_major": fields.Integer,
        "foto_profil": fields.String,
    },
)

# Model for pertanyaan
pertanyaan_model = api.model(
    "Pertanyaan",
    {
        "id_pertanyaan": fields.Integer,
        "isi_pertanyaan": fields.String(required=True),
        "kode": fields.String(required=True),
        "kelas_pertanyaan": fields.String(required=True),
    },
)

