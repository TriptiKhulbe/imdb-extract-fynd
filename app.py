import logging
import os
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, request
from flask_migrate import Migrate

from models import db

APPLICATION_ROOT = "/api"

app = Flask(__name__)
app.config.from_pyfile(
    "config" + os.path.sep + f'config.{os.environ.get("FLASK_ENV", "local")}.py'
)

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def app_index():
    req_data = {
        "Endpoint": request.endpoint,
        "Method": request.method,
        "Cookies": request.cookies.to_dict(),
        "Args": request.args.to_dict(),
        "Remote": request.remote_addr,
    }
    req_data.update(dict(request.headers))
    return req_data


@app.before_request
def before_request():
    logging.info("Request ::: %r" % request.url)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type, Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response


@app.errorhandler(Exception)
def all_exception_handler(error):
    error_message = getattr(error, "message", str(error))
    logging.getLogger("root").error(error_message, exc_info=True)
    if app.config["DEBUG"]:
        return {
            "status": "error",
            "code": 500,
            "data": {},
            "message": error_message,
        }, 500
    else:
        return (
            {
                "status": "error",
                "code": 500,
                "data": {},
                "message": "Something went wrong. "
                "Please contact the site admin.",
            },
            500,
        )


@app.errorhandler(404)
def api_not_found(error):
    error_message = getattr(error, "message", str(error))
    logging.getLogger("root").error(error_message, exc_info=True)
    return (
        {
            "status": "error",
            "code": 404,
            "data": {},
            "message": "API does not exist",
        },
        404,
    )


from routes.auth import auth
from routes.user import user
from routes.role import role
from routes.permission import permission
from routes.movie import movie

app.register_blueprint(auth, url_prefix=APPLICATION_ROOT + "/v1/auth")
app.register_blueprint(user, url_prefix=APPLICATION_ROOT + "/v1/user")
app.register_blueprint(role, url_prefix=APPLICATION_ROOT + "/v1/role")
app.register_blueprint(
    permission, url_prefix=APPLICATION_ROOT + "/v1/permission"
)
app.register_blueprint(movie, url_prefix=APPLICATION_ROOT + "/v1/movie")

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        TimedRotatingFileHandler(
            "logs/system.log", when="midnight", interval=1
        ),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9010)
