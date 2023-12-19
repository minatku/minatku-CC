from flask_restx import Resource, Namespace
from flask import request
from .extensions import authorizations, model, db
from flask_jwt_extended import jwt_required, current_user
from .models import MajorPredict
from .api_models import input_predict_model
import numpy as np
from sklearn.preprocessing import normalize
from datetime import datetime
from http import HTTPStatus
classes = ['Science', 'Arts and Literature', 'Economics', 'Technology', 'Social']

# Namespace
ns_predict = Namespace("Major_Predict", description="buat prediksi", authorizations=authorizations)

@ns_predict.route("/predict")
class PredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns_predict.doc(security="jsonWebToken")
    @ns_predict.expect(input_predict_model, validate=True)
    def post(self):
        try:
            data = request.get_json()
            input_data = data["input"]

            # Ensure input_data is a 2D array
            input_data = np.array(input_data).reshape(1, -1)

            # Normalize the input data
            fitur_normalized = normalize(input_data, axis=0)

            # Make predictions using the model
            prediction = model.predict(fitur_normalized)
            sorted_indices = np.argsort(-prediction[0])
            sorted_classes = [classes[idx] for idx in sorted_indices]
            sorted_indices = sorted_indices.tolist()

            # Format the prediction results to be returned to the client
            prediction_data = {
                "prediction_class": sorted_indices[0],
                "prediction_label": classes[sorted_indices[0]],
                "all_prediction_class": sorted_indices,
                "all_prediction_labels": sorted_classes,
            }

            save_to_database(prediction_data)

            return {
                "error": False,
                "message": "Prediction successful",
                "prediction_data": prediction_data
            }, HTTPStatus.OK
        except Exception as e:
            # Handle any exceptions and return an error message
            return {
                'error': True,
                'message': f'An error occurred: {str(e)}',
                'prediction_data': None
            }, HTTPStatus.INTERNAL_SERVER_ERROR

def save_to_database(prediction_result):
    try:

        # Create a new MajorPredict entry
        major_predict_entry = MajorPredict(
            top_1=classes[prediction_result["all_prediction_class"][0]],
            top_2=classes[prediction_result["all_prediction_class"][1]],
            top_3=classes[prediction_result["all_prediction_class"][2]],
            top_4=classes[prediction_result["all_prediction_class"][3]],
            top_5=classes[prediction_result["all_prediction_class"][4]],
            id_user=current_user.id_user,
            create_at=datetime.now()
        )

        # Add and commit the new entry to the database
        db.session.add(major_predict_entry)
        db.session.commit()
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"Error saving prediction to the database: {str(e)}")

@ns_predict.route("/major_predict/<int:user_id>")
class MajorPredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns_predict.doc(security="jsonWebToken")
    def get(self, user_id):
        try:
            # Check if the current user has the permission to access major predict data
            if current_user.id_user != user_id and not current_user.is_admin:
                return {"error": True, "message": "Unauthorized access to major predict data"}, HTTPStatus.FORBIDDEN

            # Query major predict data for the specified user ID
            major_predict_data = MajorPredict.query.filter_by(id_user=user_id).first()

            if major_predict_data:
                # Format the major predict results to be returned to the client
                result = {
                    "error": False,
                    "message": "Major predict data found",
                    "major_predict_data": {
                        "id_major_predict": major_predict_data.id_major_predict,
                        "top_1": major_predict_data.top_1,
                        "top_2": major_predict_data.top_2,
                        "top_3": major_predict_data.top_3,
                        "top_4": major_predict_data.top_4,
                        "top_5": major_predict_data.top_5,
                        "id_user": major_predict_data.id_user,
                        "create_at": major_predict_data.create_at.strftime("%Y-%m-%dT%H:%M:%S") if major_predict_data.create_at else None,
                        "update_at": major_predict_data.update_at.strftime("%Y-%m-%dT%H:%M:%S") if major_predict_data.update_at else None,
                    }
                }
                return result, HTTPStatus.OK
            else:
                return {"error": True, "message": "Major predict data not found for the specified user"}, HTTPStatus.NOT_FOUND
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
        
@ns_predict.route("/major_predict/all")
class AllMajorPredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns_predict.doc(security="jsonWebToken")
    def get(self):
        try:
            # Check if the current user has the permission to access all major predict data
            if not current_user.is_admin:
                return {"error": True, "message": "Unauthorized access to all major predict data"}, HTTPStatus.FORBIDDEN

            # Query all major predict data
            all_major_predict_data = MajorPredict.query.all()

            # Format the major predict results to be returned to the client
            results = []
            for major_predict_data in all_major_predict_data:
                result = {
                    "id_major_predict": major_predict_data.id_major_predict,
                    "top_1": major_predict_data.top_1,
                    "top_2": major_predict_data.top_2,
                    "top_3": major_predict_data.top_3,
                    "top_4": major_predict_data.top_4,
                    "top_5": major_predict_data.top_5,
                    "id_user": major_predict_data.id_user,
                    "create_at": major_predict_data.create_at.strftime("%Y-%m-%dT%H:%M:%S") if major_predict_data.create_at else None,
                    "update_at": major_predict_data.update_at.strftime("%Y-%m-%dT%H:%M:%S") if major_predict_data.update_at else None,
                }
                results.append(result)

            return {"error": False, "message": "All major predict data retrieved successfully", "major_predict_data": results}, HTTPStatus.OK
        except Exception as e:
            # Handle any exceptions and return an error message
            return {"error": True, "message": f"An error occurred: {str(e)}", "major_predict_data": None}, HTTPStatus.INTERNAL_SERVER_ERROR