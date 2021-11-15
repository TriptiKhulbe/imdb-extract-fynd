import logging

from models import db
from models.user import User, UsersRoles


class UserService:
    def __init__(self):
        self.log = logging.getLogger(__class__.__name__)

    def list_users(self):
        users = []
        for user in db.session.query(User):
            users.append(user.to_dict())
        return users

    def add_user(self, user: User):
        self._unique_email(user.email)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()

    def delete_user(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first()
        db.session.delete(user)
        db.session.commit()

    def update_user(self, user_id, *, first_name, last_name, password, email):
        user = db.session.query(User).filter(User.id == user_id).first()
        user.first_name = first_name
        user.last_name = last_name
        if user.email != email:  # by-pass validation in case of unchanged email
            self._unique_email(email)
            user.email = email
        if password:
            user.password = password
        db.session.commit()
        return user.to_dict()

    def assign_role(self, users_roles: UsersRoles):
        db.session.add(users_roles)
        db.session.commit()

    def _unique_email(self, email: str):
        if db.session.query(User).filter(User.email == email).first():
            raise AssertionError("Email address is already in use.")
