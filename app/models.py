from .extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime

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
    foto_profil = db.Column(db.String(255))
    major_predict = relationship('MajorPredict', back_populates='user')

class MajorPredict(db.Model):
    id_major_predict = db.Column(db.Integer, primary_key=True, autoincrement=True)
    top_1 = db.Column(db.String(50), nullable=False)
    top_2 = db.Column(db.String(50), nullable=False)
    top_3 = db.Column(db.String(50), nullable=False)
    top_4 = db.Column(db.String(50), nullable=False)
    top_5 = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.now, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)

    user = relationship('User', back_populates='major_predict')


class Pertanyaan(db.Model):
    id_pertanyaan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isi_pertanyaan = db.Column(db.String(255), nullable=False)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    kelas_pertanyaan = db.Column(db.String(50), nullable=False)


