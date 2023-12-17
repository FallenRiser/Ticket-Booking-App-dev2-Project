from flask import Flask, jsonify, request
from models import db, Users, Roles
import config as config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from security import *
import redis
import config
import workers
from workers import celery
from flask_restful import Resource, Api


datastore = SQLAlchemyUserDatastore(db,Users , Roles)

def create_app():
    app = Flask(__name__,  template_folder="./templates")
    CORS(app,  resources={r"/*": {"origins": "http://localhost:8080"}})
    app.config.from_object(config)
    app.secret_key = config.SECRET_KEY
    app.app_context().push()
    jwt = JWTManager(app)
    jwt.init_app(app)

    db.init_app(app)
    security.init_app(app, datastore)
    app.app_context().push()

    celery = workers.celery 
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.Task = workers.ContextTask
    app.app_context().push()

    return app, celery

app, celery = create_app()


from api_routes import *
import tasks

api = Api(app)
api_routes(api)
app.app_context().push()


""" @app.route("/hello")
def time():
    print('now in flask')
    job = tasks.send_email.apply_async(countdown = 10)
    result = job.wait()
    return str(result),200 """


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()