import logging
import time
from functools import wraps

import jwt
from flask import request, jsonify, current_app


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        end = time.time()
        logging.info("%s : %4.2f second(s)" % (func.__name__, (end - start)))
        return f

    return wrapper


def resolve_token(request):
    if request.headers.get("Authorization"):
        return request.headers.get("Authorization").split(" ")[1]
    return request.headers.get("token")


def token_required(permission_list):
    def _token_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = resolve_token(request)
            if not token:
                return (
                    {
                        "status": "error",
                        "code": 401,
                        "data": {},
                        "message": "Unauthorized access.",
                    },
                    401,
                )
            try:
                data = jwt.decode(
                    token, current_app.config["SECRET_KEY"], algorithms="HS256"
                )
                if permission_list:
                    if set(data["permissions"]).intersection(
                        set(permission_list)
                    ) != set(permission_list):
                        return {
                            "status": "error",
                            "code": 401,
                            "data": {},
                            "message": "Unauthorized access. Permission not found.",
                        }, 401
            except Exception as e:
                return {
                    "status": "error",
                    "code": 401,
                    "data": {},
                    "message": "Unauthorized access. Session expired",
                }, 401

            return func(*args, **kwargs)

        return wrapper

    return _token_required
