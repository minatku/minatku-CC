from .extensions import db

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
    
class Pertanyaan(db.Model):
    id_pertanyaan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isi_pertanyaan = db.Column(db.String(255), nullable=False)
    kode = db.Column(db.String(10), unique=True, nullable=False)
    kelas_pertanyaan = db.Column(db.String(50), nullable=False)