from flask_restx import fields

from .extensions import api 

student_model = api.model("Student", {
    "id": fields.Integer,
    "name": fields.String,
    # "course": fields.Nested(course_model)  # Uncomment this line if needed
})

course_model = api.model("Course", {
    "id": fields.Integer,
    "name": fields.String,
    "students": fields.List(fields.Nested(student_model))
})

course_input_model = api.model("CourseInput", {
    "name": fields.String,
})

student_input_model = api.model("StudentInput", {
    "name": fields.String,
    "course_id": fields.Integer
})

user_model = api.model("User", {
    "id_user": fields.Integer,
    "email": fields.String,
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
    "email": fields.String,
    "username": fields.String,
    "nama_lengkap": fields.String,
    "password": fields.String,
})
