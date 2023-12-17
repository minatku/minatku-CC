from flask_restx import Resource, Namespace
from flask import request
from .extensions import authorizations, model, db
from flask_jwt_extended import jwt_required, current_user
from .models import MajorPredict
from .api_models import input_predict_model
import numpy as np
from sklearn.preprocessing import normalize
from datetime import datetime
classes = ['Science', 'Arts and Literature', 'Economics', 'Technology', 'Social']

# Namespace
ns_predict = Namespace("Major_Predict", description="buat prediksi", authorizations=authorizations)
@ns_predict.route("/predict")
class PredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns_predict.doc(security="jsonWebToken")
    @ns_predict.expect(input_predict_model, validate=True)
    def post(self):
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
        result = {
            "prediction_class": sorted_indices[0],
            "prediction_label": classes[sorted_indices[0]],
            "all_prediction_class": sorted_indices,
            "all_prediction_labels": sorted_classes,
        }
        save_to_database(result)
        return result
def save_to_database(prediction_result):
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

@ns_predict.route("/major_predict/<int:user_id>")
class MajorPredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns_predict.doc(security="jsonWebToken")
    def get(self, user_id):
        # Check if the current user has the permission to access major predict data
        if current_user.id_user != user_id and current_user.is_admin ==False:
            return {"error": "Unauthorized access to major predict data"}, 403

        # Query major predict data for the specified user ID
        major_predict_data = MajorPredict.query.filter_by(id_user=user_id).first()

        if major_predict_data:
            # Format the major predict results to be returned to the client
            result = {
                "id_major_predict": major_predict_data.id_major_predict,
                "top_1": major_predict_data.top_1,
                "top_2": major_predict_data.top_2,
                "top_3": major_predict_data.top_3,
                "top_4": major_predict_data.top_4,
                "top_5": major_predict_data.top_5,
                "id_user":major_predict_data.id_user,
                "create_at": major_predict_data.create_at.strftime("%Y-%m-%dT%H:%M:%S") if major_predict_data.create_at else None,
                "update_at": major_predict_data.update_at.strftime("%Y-%m-%dT%H:%M:%S") if major_predict_data.update_at else None,
            }
            return result
        else:
            return {"message": "Major predict data not found for the specified user"}, 404
        
@ns_predict.route("/major_predict/all")
class AllMajorPredictResource(Resource):
    method_decorators = [jwt_required()]

    @ns_predict.doc(security="jsonWebToken")
    def get(self):
        # # Check if the current user has the permission to access all major predict data
        # if not current_user.is_admin:  # Assuming you have an 'is_admin' attribute in your User model
        #     return {"error": "Unauthorized access to all major predict data"}, 403
        if current_user.is_admin ==True:
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

            return results
        else:
            return {"message": "Unauthorized. Only admins can perform this action."}, 403