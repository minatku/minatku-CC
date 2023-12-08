from .extensions import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    students = db.relationship("Student", back_populates="course")

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    course_id = db.Column(db.ForeignKey("course.id"))

    course = db.relationship("Course", back_populates="students")

class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nama_lengkap = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    no_telepon = db.Column(db.String(15))
    lokasi = db.Column(db.String(100))
    is_premium = db.Column(db.Boolean)
    id_major = db.Column(db.Integer)
    foto_profil = db.Column(db.String(255))
