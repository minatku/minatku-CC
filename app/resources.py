from flask_restx import Resource, Namespace, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .api_models import user_model
from .extensions import db
from .models import User

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
ns = Namespace("api", authorizations=authorizations)

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}

@ns.route("/users")
class UserListAPI(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()

@ns.route("/users/<int:id>")
class UserAPI(Resource):
    method_decorators = [jwt_required()]

    @ns.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        return user

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204


@ns.route("/register")
class Register(Resource):

    @ns.expect(user_model, validate=True)
    @ns.marshal_with(user_model)
    def post(self):
        try:
            # Ambil data dari payload
            username = ns.payload["username"]
            password = ns.payload["password"]

            # Hash password
            password_hash = generate_password_hash(password)

            # Buat objek User
            user = User(username=username, password_hash=password_hash)

            # Tambahkan ke session dan commit ke database
            db.session.add(user)
            db.session.commit()

            return user, 201
        except Exception as e:
            # Tangkap kesalahan dan kirim respons kesalahan
            return {"error": str(e)}, 500


@ns.route("/login")
class Login(Resource):

    @ns.expect(user_model)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        user = User.query.filter_by(username=ns.payload["username"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, args["password"]):
            return {"error": "Incorrect password"}, 401
        return {"access_token": create_access_token(user)}

@ns.route("/all-users")
class AllUsersAPI(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()
