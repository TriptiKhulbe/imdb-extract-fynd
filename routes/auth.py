from flask import Blueprint, request
from werkzeug.security import check_password_hash

from services.auth_service import AuthService

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["POST"])
def authenticate():
    username = request.args.get("username")
    password = request.args.get("password")
    service = AuthService()
    response = service.authenticate(username, password, check_password_hash)
    return {
        "status": "success",
        "data": response,
        "message": "Welcome %s!!" % response.get("first_name", "N/A"),
    }
