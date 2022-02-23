import sqlite3
from time import ctime

import bcrypt
from bottle import static_file, Bottle, view, auth_basic, request, abort

from src.db.db import Db

START_TIME = None
password_hash_cache = {}


def init(cfg):
    global START_TIME
    START_TIME = ctime()


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    @view("index.tpl")
    @auth_basic(auth_check)
    def index():
        username = request.auth[0]
        with Db(auto_commit=False) as db:
            current_user_role = db.get_user_role_from_username(username)
            if current_user_role in ["god", "admin"]:
                users = list(db.get_users())
            else:
                users = []
        if users:
            # Sort users by role
            users = sorted(users, key=lambda u: ({"god": 0, "admin": 1, "user": 2}[u["role"]], u["id"]))
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

    @app.post("/add_new_user")
    @view("redirect_to_main.tpl")
    @auth_basic(auth_check)
    def add_new_user():
        current_user = request.auth[0]
        new_username = request.forms["username"].lower()
        new_user_role = request.forms["role"].lower()
        with Db() as db:
            current_user_role = db.get_user_role_from_username(current_user)
            if current_user_role == "user":
                abort(403, "Sorry, only admins can edit users.")
            elif current_user_role == "admin" and new_user_role == "admin":
                abort(403, "Sorry, admins cannot create other admins.")
            elif new_user_role not in ["admin", "user"]:
                abort(403, f"{new_user_role} is not a valid role.")
            try:
                db.add_user(
                    new_username,
                    request.forms["full_name"],
                    bcrypt.hashpw(request.forms["password"].encode(), bcrypt.gensalt()),
                    new_user_role
                )
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: users.username":
                    abort(400, f"A user with the username '{new_username}' already exists.")
                raise
        return {
            "title": f"Added user '{new_username}'",
            "message": f"'{new_username}' has been added to the database."
        }

    @app.get("/delete_user/<user_id>")
    @view("redirect_to_main.tpl")
    @auth_basic(auth_check)
    def delete_user(user_id):
        with Db() as db:
            _admin_check(db, request.auth[0], user_id)
            response = db.delete_user(user_id)
            if response is None:
                abort(400, f"No user found with id={user_id}")
        return {
            "title": f"Deleted user id={user_id}",
            "message": f"User with id='{user_id}' has been deleted."
        }

    @app.get("/change_username/<user_id>/<username>")
    @view("redirect_to_main.tpl")
    @auth_basic(auth_check)
    def change_username(user_id, username):
        with Db() as db:
            _admin_check(db, request.auth[0], user_id)
            if not username:
                abort(400, f"{username} is not a valid username.")
            try:
                response = db.change_username(user_id, username)
                if response is None:
                    abort(400, f"No user found with id={user_id}")
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: users.username":
                    abort(400, f"A user with the username '{username}' already exists.")
                raise
        return {
            "title": f"Changed user id={user_id} username to '{username}'",
            "message": f"User with id='{user_id}' has had their username changed to '{username}'."
        }


def _admin_check(db, current_user: str, user_id: int):
    current_user_role = db.get_user_role_from_username(current_user)
    if current_user_role == "user":
        abort(403, "Sorry, only admins can edit users.")
    elif current_user_role == "admin" and db.get_user_role_from_id(user_id) == "admin":
        abort(403, "Sorry, admins cannot edit other admins.")


def password_check(password, password_hash):
    return password_hash is not None and bcrypt.checkpw(password.encode("utf-8"), password_hash)


def auth_check(username, password):
    if username not in password_hash_cache or not password_check(password, password_hash_cache[username]):
        with Db(auto_commit=False) as db:
            password_hash_cache[username] = db.get_password_hash_for_username(username)
    return password_check(password, password_hash_cache[username])
