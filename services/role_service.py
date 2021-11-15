import logging
from typing import List

from models import db
from models.user import Role, Permission


class RoleService:
    def __init__(self):
        self.log = logging.getLogger(__class__.__name__)

    def list_roles(self):
        roles = []
        for role in db.session.query(Role):
            roles.append(role.to_dict())
        return roles

    def add_role(self, role: Role):
        db.session.add(role)
        db.session.commit()
        return role.to_dict()

    def delete_role(self, role_id):
        role = db.session.query(Role).filter(Role.id == role_id).first()
        db.session.delete(role)
        db.session.commit()

    def update_role(self, role_id, *, name, label):
        role = db.session.query(Role).filter(Role.id == role_id).first()
        role.name = name
        role.label = label
        db.session.commit()
        return role.to_dict()

    def add_permissions(self, role_id: int, permissions: List[Permission]):
        role = db.session.query(Role).filter(Role.id == role_id).first()
        role.permissions = permissions
        db.session.commit()
        return role.to_dict()
