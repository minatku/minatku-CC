from flask_restx import fields

from .extensions import api 

user_model = api.model("UserModel", {
    "id_user": fields.Integer,
    "username": fields.String,
    "nama_lengkap": fields.String,
    "password": fields.String,
    "tanggal_lahir": fields.Date,
    "gender": fields.String,
    "no_telepon": fields.String,
    "lokasi": fields.String,
    "is_premium": fields.Boolean,
    "id_major": fields.Integer,
    "foto_profil": fields.String
})

user_input_model = api.model("UserInput", {
    "username": fields.String,
    "nama_lengkap": fields.String,
    "password": fields.String,
    "tanggal_lahir": fields.Date,
    "gender": fields.String,
    "no_telepon": fields.String,
    "lokasi": fields.String,
    "is_premium": fields.Boolean,
    "id_major": fields.Integer,
    "foto_profil": fields.String
})
