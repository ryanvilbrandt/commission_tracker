from time import ctime

import bcrypt
from bottle import static_file, Bottle, view, auth_basic, request

from src.db.db import Db

START_TIME = None

websocket_list = []


def init(cfg):
    global START_TIME
    START_TIME = ctime()


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    @view("index.tpl")
    @auth_basic(auth_check)
    def index():
        username = request.auth[0]
        with Db() as db:
            current_user_role = db.get_user_role(username)
            if current_user_role in ["god", "admin"]:
                users = list(db.get_users())
            else:
                users = []
        if users:
            # Sort users by role
            users = sorted(users, key=lambda u: {"god": 0, "admin": 1, "user": 2}[u["role"]])
            # Determine if user buttons should be enabled or disabled for each user
            for user in users:
                if user["role"] == "god":
                    disable_user_buttons = True
                elif user["role"] == "admin":
                    disable_user_buttons = current_user_role != "god"
                else:
                    disable_user_buttons = False
                user["disable_user_buttons"] = disable_user_buttons
        return {"title": "Home page!", "users": users}

    @app.get("/static/<path:path>", name="static")
    @auth_basic(auth_check)
    def static(path):
        return static_file(path, root="static")

    @app.get("/favicon.ico", name="favicon")
    @auth_basic(auth_check)
    def favicon():
        return static_file("favicon.ico", root="static")


def auth_check(username, password):
    with Db(auto_commit=False) as db:
        password_hash = db.get_password_hash_for_username(username)
    return password_hash is not None and bcrypt.checkpw(password.encode("utf-8"), password_hash)
