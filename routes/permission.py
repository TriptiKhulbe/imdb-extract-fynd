from flask import Blueprint, request

from models.user import Permission
from services.permission_service import PermissionService
from utils.decorators import token_required

permission = Blueprint("permission", __name__)


@permission.route("/", methods=["GET"])
@token_required(["CRUD_PERMISSION"])
def list_permissions():
    service = PermissionService()
    response = service.list_permissions()
    return {
        "status": "success",
        "data": response,
        "message": "",
    }


@permission.route("/", methods=["POST"])
@token_required(["CRUD_PERMISSION"])
def add_permission():
    request_args = request.get_json()
    permission = Permission(name=request_args.get("name"))
    service = PermissionService()
    response = service.add_permission(permission)
    return {
        "status": "success",
        "data": response,
        "message": "Permission added.",
    }


@permission.route("/<permission_id>", methods=["PUT"])
@token_required(["CRUD_PERMISSION"])
def update_permission(permission_id):
    request_args = request.get_json()
    service = PermissionService()
    response = service.update_permission(
        permission_id, name=request_args.get("name")
    )
    return {
        "status": "success",
        "data": response,
        "message": "Permission updated.",
    }


@permission.route("/<permission_id>", methods=["DELETE"])
@token_required(["CRUD_PERMISSION"])
def delete_permissions(permission_id):
    service = PermissionService()
    service.delete_permission(permission_id)
    return {
        "status": "success",
        "data": {},
        "message": "Permission deleted.",
    }
