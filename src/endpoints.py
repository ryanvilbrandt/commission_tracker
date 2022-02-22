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
        return {"title": "Home page!", "username": request.auth[0]}

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
