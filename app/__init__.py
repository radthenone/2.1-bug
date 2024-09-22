import json
import typing

from auth.route import LoginController
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.auth.route import LogoutController, RegisterController
from app.config import Config
from app.database import db
from app.tasks.db import TaskModel
from app.todos.db import TodoModel
from app.todos.route import TodoController
from app.users.db import UserModel

app = Flask(__name__, instance_relative_config=True)
app.config["TESTING"] = True
app.config.update(Config().to_dict())
db.init_app(app)
with app.app_context():
    db.create_all()

Migrate(app, db)
api = Api(app)


api.add_resource(LogoutController, "/auth/logout", endpoint="logout")
api.add_resource(LoginController, "/auth/login", endpoint="login")
api.add_resource(RegisterController, "/auth/register", endpoint="register")

api.add_resource(TodoController, "/todos", "/todos/<int:todo_id>")

__all__ = ["app"]
