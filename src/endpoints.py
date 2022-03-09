import sqlite3
from time import ctime
from typing import Optional, List

import bcrypt
from bottle_websocket import websocket

from bottle import static_file, Bottle, view, auth_basic, request, abort, template
from src import utils
from src.db.db import Db

START_TIME = None
password_hash_cache = {}


def init(cfg):
    global START_TIME
    START_TIME = ctime()


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    @view("index.tpl")
    @auth_basic(_auth_check)
    def index():
        username = request.auth[0]
        with Db(auto_commit=False) as db:
            current_user = _get_user(db, username)
            if current_user["role"] in ["god", "admin"]:
                users = list(db.get_users())
            else:
                users = []
            commissions = _fetch_commissions(db, current_user, [])
        if users:
            # Sort users by role
            users = sorted(users, key=lambda u: ({"god": 0, "admin": 1, "user": 2}[u["role"]], u["id"]))
            # Determine if user buttons should be enabled or disabled for each user
            for user in users:
                if user["role"] == "god":
                    disable_user_buttons = True
                elif user["role"] == "admin":
                    disable_user_buttons = current_user["role"] != "god"
                else:
                    disable_user_buttons = False
                user["disable_user_buttons"] = disable_user_buttons
        return {"title": "Home page!", "users": users, "current_user": current_user, "commissions": commissions}

    @app.get("/static/<path:path>", name="static")
    def static(path):
        return static_file(path, root="static")

    @app.get("/favicon.ico", name="favicon")
    def favicon():
        return static_file("favicon.ico", root="static")

    @app.get("/fetch_commissions/<opened_details>")
    @view("commissions.tpl")
    @auth_basic(_auth_check)
    def fetch_commissions(opened_details):
        with Db() as db:
            current_user = db.get_user_from_username(request.auth[0])
            commissions = _fetch_commissions(
                db, current_user, [] if opened_details == "_" else opened_details.split(",")
            )
        return {"commissions": commissions}

    @app.get('/commissions_websocket', apply=[websocket])
    @auth_basic(_auth_check)
    def commissions_websocket(ws):
        utils.websocket_loop(ws)

    @app.get("/send_to_websockets")
    @auth_basic(_auth_check)
    def send_to_websockets():
        utils.send_to_websockets("refresh")

    @app.post("/add_new_user")
    @view("redirect_to_main.tpl")
    @auth_basic(_auth_check)
    def add_new_user():
        current_user = request.auth[0]
        new_username = request.forms["username"].lower()
        new_user_role = request.forms["role"].lower()
        with Db() as db:
            _permissions_check(db, request.auth[0])
            current_user_role = db.get_user_role_from_username(current_user)
            if current_user_role == "user":
                abort(403, "Sorry, only admins can create users.")
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
    @auth_basic(_auth_check)
    def delete_user(user_id):
        with Db() as db:
            _permissions_check(db, request.auth[0], user_id, allow_change_self=False)
            response = db.delete_user(user_id)
            if response is None:
                abort(400, f"No user found with id={user_id}")
        return {
            "title": f"Deleted user id={user_id}",
            "message": f"User with id='{user_id}' has been deleted."
        }

    @app.get("/change_username/<user_id>/<username>")
    @auth_basic(_auth_check)
    def change_username(user_id, username):
        with Db() as db:
            change_self = _permissions_check(db, request.auth[0], user_id)
            if not username:
                abort(400, f"{username} is not a valid username.")
            old_username = db.get_username_from_id(user_id)
            try:
                response = db.change_username(user_id, username.lower())
                if response is None:
                    abort(400, f"No user found with id={user_id}")
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: users.username":
                    abort(400, f"A user with the username '{username}' already exists.")
                raise
        _delete_from_password_cache(old_username)
        if change_self:
            return template("logout.tpl", {
                "title": "Username successfully changed",
                "message": f"Your username has been changed to '{username}'!"
            })
        else:
            return template("redirect_to_main.tpl", {
                "title": f"Changed user id={user_id} username to '{username}'",
                "message": f"User with id='{user_id}' has had their username changed to '{username}'. "
                           f"The user will need to restart their web browser to log back into the website.",
            })

    @app.get("/change_full_name/<user_id>/<full_name>")
    @view("redirect_to_main.tpl")
    @auth_basic(_auth_check)
    def change_full_name(user_id, full_name):
        with Db() as db:
            change_self = _permissions_check(db, request.auth[0], user_id)
            if not full_name:
                abort(400, f"{full_name} is not a valid name.")
            response = db.change_full_name(user_id, full_name)
            if response is None:
                abort(400, f"No user found with id={user_id}")
        if change_self:
            return {
                "title": "Full name successfully changed",
                "message": f"Your name has been changed to '{full_name}'!",
            }
        else:
            return {
                "title": f"Changed user id={user_id} full name to '{full_name}'",
                "message": f"User with id='{user_id}' has had their full name changed to '{full_name}'.",
            }

    @app.get("/change_password/<user_id>/<password>")
    @auth_basic(_auth_check)
    def change_password(user_id, password):
        with Db() as db:
            change_self = _permissions_check(db, request.auth[0], user_id)
            if not password:
                abort(400, f"{password} is not a valid password.")
            response = db.change_password(user_id, bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
            if response is None:
                abort(400, f"No user found with id={user_id}")
            username = db.get_username_from_id(user_id)
        _delete_from_password_cache(username)
        if change_self:
            return template("logout.tpl", {
                "title": "Password successfully changed",
                "message": "Your password has been changed!",
            })
        else:
            return template("redirect_to_main.tpl", {
                "title": f"Changed user id={user_id} password",
                "message": f"User with id='{user_id}' has had their password changed. "
                           f"The user will need to restart their web browser to log back into the website.",
            })

    @app.error(401)
    @view("error_401.tpl")
    def invalid_user(*args):
        if request.auth is not None:
            _delete_from_password_cache(request.auth[0])


def _get_user(db: Db, username: str):
    current_user = db.get_user_from_username(username)
    if current_user is None:
        _delete_from_password_cache(username)
        abort(401)
    return current_user


def _permissions_check(db, username: str, user_id: Optional[int]=None, allow_change_self=True) -> bool:
    """
    Returns True if the user is trying to edit themselves, False otherwise. Raises a 403 HTTPError if
    they are not allowed to perform the current operation.
    """
    current_user = _get_user(db, username)
    if allow_change_self and str(current_user["id"]) == user_id:
        return True
    if current_user["role"] == "user":
        abort(403, "Sorry, only admins can edit users.")
    if current_user["role"] == "admin" and db.get_user_role_from_id(user_id) == "admin":
        abort(403, "Sorry, admins cannot edit other admins.")
    return str(current_user["id"]) == user_id


def _password_check(password, password_hash):
    return password_hash is not None and bcrypt.checkpw(password.encode("utf-8"), password_hash)


def _auth_check(username, password):
    if username not in password_hash_cache or not _password_check(password, password_hash_cache[username]):
        with Db(auto_commit=False) as db:
            password_hash_cache[username] = db.get_password_hash_for_username(username)
    return _password_check(password, password_hash_cache[username])


def _delete_from_password_cache(username):
    if username in password_hash_cache:
        del password_hash_cache[username]


def _fetch_commissions(db: Db, current_user: dict, opened_commissions: List[str]):
    my_commissions = []
    available_commissions = []
    other_commissions = []
    for commission in db.get_all_commissions_with_users():
        # Modify data
        if str(commission["id"]) in opened_commissions:
            commission["open"] = True
        if commission["assigned_to"] == -1:
            commission["assigned_string"] = "Unassigned"
        else:
            commission["assigned_string"] = "Assigned to {}".format(commission["full_name"])
        commission["reference_images"] = commission["reference_images"].split(", ")
        # Assign to queue
        if commission["assigned_to"] == current_user["id"]:
            commission["claimable"] = False
            my_commissions.append(commission)
        elif commission["assigned_to"] == -1 and commission["allow_any_artist"]:  # Unassigned and claimable
            commission["claimable"] = True
            available_commissions.append(commission)
        else:
            commission["claimable"] = True
            other_commissions.append(commission)
    return {
        "my_commissions": my_commissions,
        "available_commissions": available_commissions,
        "other_commissions": other_commissions
    }