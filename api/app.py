import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
api = Api(app)

load_dotenv()


class User:
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(id='{self.id}')"


USERS = [
    User(1, "admin", os.getenv("ADMIN_PASSWORD")),
]

username_table = {u.username: u for u in USERS}
userid_table = {u.id: u for u in USERS}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode("utf-8"), password.encode("utf-8")):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_table.get(user_id, None)


app.config["SECRET_KEY"] = os.getenv("APP_CONFIG_KEY")
admin = JWT(app, authentication_handler=authenticate, identity_handler=identity)


if __name__ == "__main__":
    app.run(debug=True)
