import re

from sqlalchemy import (
    Column,
    String,
    Integer,
    Sequence,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship, validates

from models import db


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    # Relationships
    roles = relationship(
        "Role",
        secondary="users_roles",
        backref=db.backref("users", lazy="dynamic"),
    )

    def __init__(self, first_name, last_name, email, password, *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User - %s %s>" % (self.first_name, self.last_name)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": "*****",
            "roles": [role.to_dict() for role in self.roles],
        }

    @validates("first_name", "last_name")
    def validate_length(self, key, field):
        if not field:
            raise AssertionError(f"No {key} provided.")
        if len(field) > 80:
            raise AssertionError(f"{key} must be less than 80 characters")
        return field

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise AssertionError(f"No email provided.")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not an email address.")
        return email


class Role(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    label = Column(String(80), nullable=False)

    # Relationships
    permissions = relationship(
        "Permission",
        secondary="roles_permissions",
        backref=db.backref("roles", lazy="dynamic"),
    )

    def __init__(self, name, label, *args, **kwargs):
        self.name = name
        self.label = label

    def __repr__(self):
        return "<Role - %s>" % self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "permissions": [
                permission.to_dict() for permission in self.permissions
            ],
        }


class UsersRoles(db.Model):
    __tablename__ = "users_roles"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"))
    role_id = Column(Integer(), ForeignKey("roles.id", ondelete="CASCADE"))


class Permission(db.Model):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return "<Permission - %s>" % self.name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class RolesPermissions(db.Model):
    __tablename__ = "roles_permissions"

    id = Column(Integer(), primary_key=True)
    role_id = Column(Integer(), ForeignKey("roles.id", ondelete="CASCADE"))
    permission_id = Column(
        Integer(), ForeignKey("permissions.id", ondelete="CASCADE")
    )
