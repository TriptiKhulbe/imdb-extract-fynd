import logging
from typing import List

from models import db
from models.user import Permission


class PermissionService:
    def __init__(self):
        self.log = logging.getLogger(__class__.__name__)

    def list_permissions(self):
        permissions = []
        for permission in db.session.query(Permission):
            permissions.append(permission.to_dict())
        return permissions

    def add_permission(self, permission: Permission):
        db.session.add(permission)
        db.session.commit()
        return permission.to_dict()

    def delete_permission(self, permission_id):
        permission = (
            db.session.query(Permission)
            .filter(Permission.id == permission_id)
            .first()
        )
        db.session.delete(permission)
        db.session.commit()

    def update_permission(self, permission_id, *, name):
        permission = (
            db.session.query(Permission)
            .filter(Permission.id == permission_id)
            .first()
        )
        permission.name = name
        db.session.commit()
        return permission.to_dict()

    def merge_permission(self, permissions: List[str]):
        permissions_found = (
            db.session.query(Permission)
            .filter(Permission.name.in_(permissions))
            .all()
        )
        permissions_new = [
            Permission(name)
            for name in set(permissions).difference(
                set(map(lambda x: str(x), permissions_found))
            )
        ]
        db.session.add_all(permissions_new)
        return permissions_new + permissions_found
