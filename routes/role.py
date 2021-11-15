from flask import Blueprint, request

from models.user import Role
from services.permission_service import PermissionService
from services.role_service import RoleService
from utils.decorators import token_required

role = Blueprint("role", __name__)


@role.route("/", methods=["GET"])
@token_required(["CRUD_ROLE"])
def list_roles():
    service = RoleService()
    response = service.list_roles()
    return {
        "status": "success",
        "data": response,
        "message": "",
    }


@role.route("/", methods=["POST"])
@token_required(["CRUD_ROLE"])
def add_role():
    request_args = request.get_json()
    role = Role(name=request_args.get("name"), label=request_args.get("label"))
    service = RoleService()
    response = service.add_role(role)
    return {
        "status": "success",
        "data": response,
        "message": "Role added.",
    }


@role.route("/<role_id>", methods=["PUT"])
@token_required(["CRUD_ROLE"])
def update_role(role_id):
    request_args = request.get_json()
    service = RoleService()
    response = service.update_role(
        role_id, name=request_args.get("name"), label=request_args.get("label")
    )
    return {
        "status": "success",
        "data": response,
        "message": "Role updated.",
    }


@role.route("/<role_id>", methods=["DELETE"])
@token_required(["CRUD_ROLE"])
def delete_roles(role_id):
    service = RoleService()
    service.delete_role(role_id)
    return {
        "status": "success",
        "data": {},
        "message": "Role deleted.",
    }


@role.route("/<role_id>/add_permission", methods=["POST"])
@token_required(["CRUD_ROLE"])
def add_permissions(role_id):
    request_args = request.get_json()
    permissions = PermissionService().merge_permission(
        request_args.get("permissions")
    )
    service = RoleService()
    response = service.add_permissions(role_id, permissions)
    return {
        "status": "success",
        "data": response,
        "message": "Permission added to the role.",
    }
