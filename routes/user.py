from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from models.user import User, UsersRoles
from services.user_service import UserService
from utils.decorators import token_required

user = Blueprint("user", __name__)


@user.route("/", methods=["GET"])
def list_users():
    service = UserService()
    response = service.list_users()
    return {
        "status": "success",
        "data": response,
        "message": "",
    }


@user.route("/", methods=["POST"])
def add_user():
    request_args = request.get_json()
    user = User(
        first_name=request_args.get("first_name"),
        last_name=request_args.get("last_name"),
        email=request_args.get("email"),
        password=generate_password_hash(request_args.get("password")),
    )
    service = UserService()
    response = service.add_user(user)
    return {
        "status": "success",
        "data": response,
        "message": "User added.",
    }


@user.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    request_args = request.get_json()
    password = request_args.get("password")
    if password:
        hashed_password = generate_password_hash(password)
    else:
        hashed_password = None
    service = UserService()
    response = service.update_user(
        user_id,
        first_name=request_args.get("first_name"),
        last_name=request_args.get("last_name"),
        email=request_args.get("email"),
        password=hashed_password,
    )
    return {
        "status": "success",
        "data": response,
        "message": "User updated.",
    }


@user.route("/<user_id>", methods=["DELETE"])
@token_required(["REMOVE_USER"])
def delete_users(user_id):
    service = UserService()
    service.delete_user(user_id)
    return {
        "status": "success",
        "data": {},
        "message": "User deleted.",
    }


@user.route("/<user_id>/assign_role/<role_id>", methods=["POST"])
@token_required(["ASSIGN_ROLE"])
def assign_role(user_id, role_id):
    users_roles = UsersRoles(user_id=user_id, role_id=role_id)
    service = UserService()
    service.assign_role(users_roles)
    return {
        "status": "success",
        "data": {},
        "message": "Role assigned to the user.",
    }
