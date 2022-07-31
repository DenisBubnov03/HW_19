from flask import request
from flask_restx import Resource, Namespace

from containers import user_service
from dao.model.user import UserSchema

user_ns = Namespace('users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()
        users = users_schema.dump(all_users)
        return users, 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>/')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        sm_d = UserSchema().dump(user)
        return sm_d, 200

    def put(self, uid):
        data = request.json

        if data.get("id") == None:
            data["id"] = uid

        user_service.update(data)
        return "", 204

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
