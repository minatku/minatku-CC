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
    gender = db.Column(db.Enum('Laki-laki', 'Perempuan', 'Lainnya'))
    no_telepon = db.Column(db.String(15))
    lokasi = db.Column(db.String(100))
    is_premium = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean, default=False)  # Kolom baru untuk menentukan apakah user adalah admin
    foto_profil = db.Column(db.String(255))
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime)

class MajorPredict(db.Model):
    id_major_predict = db.Column(db.Integer, primary_key=True, autoincrement=True)
    top_1 = db.Column(db.String(50), nullable=False)
    top_2 = db.Column(db.String(50), nullable=False)
    top_3 = db.Column(db.String(50), nullable=False)
    top_4 = db.Column(db.String(50), nullable=False)
    top_5 = db.Column(db.String(50), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime)

class Pertanyaan(db.Model):
    id_pertanyaan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isi_pertanyaan = db.Column(db.String(255), nullable=False)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    kelas_pertanyaan = db.Column(db.String(50), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime)
