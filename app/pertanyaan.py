from flask_restx import Resource, Namespace
from flask import request
from .extensions import db
from .models import Pertanyaan
from .api_models import pertanyaan_model
ns_pertanyaan = Namespace("Pertanyaan", description="data buat assesment")

@ns_pertanyaan.route("/pertanyaan")
class PertanyaanResource(Resource):
    @ns_pertanyaan.expect(pertanyaan_model, validate=True)
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
    
@ns_pertanyaan.route("/pertanyaan/<int:id_pertanyaan>")
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

