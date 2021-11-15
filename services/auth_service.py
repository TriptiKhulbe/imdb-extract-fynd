import logging
import datetime

import jwt
from flask import current_app

from models import db
from models.user import User
from utils.exceptions import InvalidCredentials


class AuthService:
    def __init__(self):
        self.log = logging.getLogger(__class__.__name__)

    def authenticate(self, username: str, password: str, check_strategy):
        user = db.session.query(User).filter(User.email == username).first()
        is_valid = check_strategy(user.password, password)
        if not is_valid:
            raise InvalidCredentials()

        # generate token with permission set
        roles = []
        permissions = []
        for role in user.roles:
            roles.append(role.name)
            for permission in role.permissions:
                permissions.append(permission.name)

        token = jwt.encode(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "permissions": permissions,
                "roles": roles,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=4),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return {**user.to_dict(), "token": token}
