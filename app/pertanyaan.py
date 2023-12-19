from flask_restx import Resource, Namespace
from flask import request
from .extensions import db, authorizations
from .models import Pertanyaan
from .api_models import pertanyaan_model, pertanyaan_edit_model
from flask_jwt_extended import jwt_required, current_user
from http import HTTPStatus

ns_pertanyaan = Namespace("Pertanyaan", description="data buat assesment", authorizations=authorizations)

@ns_pertanyaan.route("/pertanyaan")
class PertanyaanResource(Resource):
    method_decorators = [jwt_required()]

    @ns_pertanyaan.doc(security="jsonWebToken")
    @ns_pertanyaan.expect(pertanyaan_model, validate=True)
    def post(self):
        try:
            if current_user.is_admin == True:
                data = request.get_json()
                new_pertanyaan = Pertanyaan(
                    isi_pertanyaan=data["isi_pertanyaan"],
                    kode=data["kode"],
                    kelas_pertanyaan=data["kelas_pertanyaan"],
                )
                db.session.add(new_pertanyaan)
                db.session.commit()
                return {"error": False, "message": "Pertanyaan created successfully"}, HTTPStatus.CREATED
            else:
                return {"error": True, "message": "Unauthorized. Only admins can perform this action."}, HTTPStatus.FORBIDDEN
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    method_decorators = [jwt_required()]
    @ns_pertanyaan.doc(security="jsonWebToken")
    def get(self):
        try:
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
            return {"error": False, "message": "Pertanyaan data retrieved successfully", "pertanyaan_data": pertanyaan_data}, HTTPStatus.OK
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}", "pertanyaan_data": None}, HTTPStatus.INTERNAL_SERVER_ERROR
    
@ns_pertanyaan.route("/pertanyaan/<int:id_pertanyaan>")
class PertanyaanByIdResource(Resource):
    method_decorators = [jwt_required()]

    @ns_pertanyaan.doc(security="jsonWebToken")
    def get(self, id_pertanyaan):
        try:
            pertanyaan = Pertanyaan.query.get(id_pertanyaan)
            if pertanyaan:
                pertanyaan_data = {
                    "error": False,
                    "message": "Pertanyaan found",
                    "pertanyaan_data": {
                        "id_pertanyaan": pertanyaan.id_pertanyaan,
                        "isi_pertanyaan": pertanyaan.isi_pertanyaan,
                        "kode": pertanyaan.kode,
                        "kelas_pertanyaan": pertanyaan.kelas_pertanyaan,
                    }
                }
                return pertanyaan_data, HTTPStatus.OK
            else:
                return {"error": True, "message": "Pertanyaan not found", "pertanyaan_data": None}, HTTPStatus.NOT_FOUND
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}", "pertanyaan_data": None}, HTTPStatus.INTERNAL_SERVER_ERROR

    method_decorators = [jwt_required()]
    @ns_pertanyaan.doc(security="jsonWebToken")
    @ns_pertanyaan.expect(pertanyaan_edit_model, validate=True)
    def put(self, id_pertanyaan):
        try:
            if current_user.is_admin == True:
                pertanyaan = Pertanyaan.query.get(id_pertanyaan)
                if pertanyaan:
                    data = request.get_json()
                    # Update pertanyaan information based on the received data
                    pertanyaan.isi_pertanyaan = data.get("isi_pertanyaan", pertanyaan.isi_pertanyaan)
                    pertanyaan.kode = data.get("kode", pertanyaan.kode)
                    pertanyaan.kelas_pertanyaan = data.get("kelas_pertanyaan", pertanyaan.kelas_pertanyaan)
                    db.session.commit()
                    return {"error": False, "message": "Pertanyaan updated successfully"}, HTTPStatus.OK
                else:
                    return {"error": True, "message": "Pertanyaan not found"}, HTTPStatus.NOT_FOUND
            else:
                return {"error": True, "message": "Unauthorized. Only admins can perform this action."}, HTTPStatus.FORBIDDEN
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    method_decorators = [jwt_required()]
    @ns_pertanyaan.doc(security="jsonWebToken")
    def delete(self, id_pertanyaan):
        try:
            if current_user.is_admin == True:
                pertanyaan = Pertanyaan.query.get(id_pertanyaan)
                if pertanyaan:
                    db.session.delete(pertanyaan)
                    db.session.commit()
                    return {"error": False, "message": "Pertanyaan deleted successfully"}, HTTPStatus.OK
                else:
                    return {"error": True, "message": "Pertanyaan not found"}, HTTPStatus.NOT_FOUND
            else:
                return {"error": True, "message": "Unauthorized. Only admins can perform this action."}, HTTPStatus.FORBIDDEN
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

