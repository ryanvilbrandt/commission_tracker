import os
import sqlite3
import sys
from collections import defaultdict
from json import loads
from time import ctime, mktime, strptime
from typing import Optional, List, Dict

import bcrypt
from bottle import static_file, Bottle, auth_basic, request, abort
from bottle_websocket import websocket
from mako.lookup import TemplateLookup
from markdown2 import Markdown
from pyinstrument import Profiler

from src import utils, functions
from src.db.db import Db

ENABLE_PROFILING = False

START_TIME = None
MD: Optional[Markdown] = None
HOST_QUICK_GUIDE_MD = None
USER_QUICK_GUIDE_MD = None
HOST_HELP_MD = None
USER_HELP_MD = None
TEMPLATE_LOOKUP = None
password_hash_cache = {}


def init(cfg):
    global START_TIME, MD, HOST_QUICK_GUIDE_MD, USER_QUICK_GUIDE_MD, HOST_HELP_MD, USER_HELP_MD, TEMPLATE_LOOKUP
    START_TIME = ctime()
    MD = Markdown(extras=["break-on-newline"])
    with open("src/host_quick_guide.md", "rb") as f:
        HOST_QUICK_GUIDE_MD = MD.convert(f.read())
    with open("src/user_quick_guide.md", "rb") as f:
        USER_QUICK_GUIDE_MD = MD.convert(f.read())
    with open("src/host_help.md", "rb") as f:
        HOST_HELP_MD = MD.convert(f.read())
    with open("src/user_help.md", "rb") as f:
        USER_HELP_MD = MD.convert(f.read())
    TEMPLATE_LOOKUP = TemplateLookup(directories=['views'])


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @auth_basic(_auth_check)
    def index():
        if ENABLE_PROFILING:
            profiler = Profiler()
            profiler.start()
        username = request.auth[0]
        with Db(auto_commit=False) as db:
            current_user = _get_user(db, username)
            users = _get_users(db, current_user)
            commissions = _fetch_commissions(db, current_user, [], [])
        t = TEMPLATE_LOOKUP.get_template("index.tpl")
        r = t.render(
            title="Commission Tracker",
            users=users,
            current_user=current_user,
            commissions=commissions,
            host_quick_guide=HOST_QUICK_GUIDE_MD,
            user_quick_guide=USER_QUICK_GUIDE_MD,
        )
        if ENABLE_PROFILING:
            profiler.stop()
            print(profiler.output_text(unicode=True, color=True))
        return r

    @app.get("/host_help")
    @auth_basic(_auth_check)
    def host_help():
        t = TEMPLATE_LOOKUP.get_template("md_page.tpl")
        return t.render(title="Commission Tracker Help for Hosts", md=HOST_HELP_MD)

    @app.get("/user_help")
    @auth_basic(_auth_check)
    def host_help():
        t = TEMPLATE_LOOKUP.get_template("md_page.tpl")
        return t.render(title="Commission Tracker Help for Artists", md=USER_HELP_MD)

    @app.get("/static/<path:path>", name="static")
    def static(path):
        return static_file(path, root="static")

    @app.get("/get_finished_commission_image/<path:path>")
    def static(path):
        return static_file(path, root="finished_commissions")

    @app.get("/favicon.ico", name="favicon")
    def favicon():
        return static_file("favicon.ico", root="static")

    @app.get("/fetch_commissions/<opened_details>/<hidden_queues>")
    @auth_basic(_auth_check)
    def fetch_commissions(opened_details, hidden_queues):
        if ENABLE_PROFILING:
            profiler = Profiler()
            profiler.start()
        with Db() as db:
            current_user = db.get_user_from_username(request.auth[0])
            users = _get_users(db, current_user)
            commissions = _fetch_commissions(
                db,
                current_user,
                [] if opened_details == "_" else opened_details.split(","),
                [] if hidden_queues == "_" else hidden_queues.split(",")
            )
        t = TEMPLATE_LOOKUP.get_template("commissions.tpl")
        r = t.render(
            users=users,
            current_user=current_user,
            commissions=commissions,
        )
        if ENABLE_PROFILING:
            profiler.stop()
            print(profiler.output_text(unicode=True, color=True))
        return r

    @app.get("/fetch_users")
    @auth_basic(_auth_check)
    def fetch_users():
        if ENABLE_PROFILING:
            profiler = Profiler()
            profiler.start()
        with Db() as db:
            current_user = db.get_user_from_username(request.auth[0])
            users = _get_users(db, current_user)
        t = TEMPLATE_LOOKUP.get_template("users.tpl")
        r = t.render(users=users)
        if ENABLE_PROFILING:
            profiler.stop()
            print(profiler.output_text(unicode=True, color=True))
        return r

    @app.get("/fetch_queue_open")
    @auth_basic(_auth_check)
    def fetch_queue_open():
        with Db() as db:
            current_user = db.get_user_from_username(request.auth[0])
        return "true" if current_user["queue_open"] else "false"

    @app.get('/commissions_websocket', apply=[websocket])
    @auth_basic(_auth_check)
    def commissions_websocket(ws):
        ws.send("ping")
        utils.websocket_loop(ws)

    @app.get("/send_to_websockets")
    @auth_basic(_auth_check)
    def send_to_websockets():
        with Db() as db:
            _permissions_check(db, request.auth[0])
        utils.send_to_websockets("refresh")

    @app.get("/commission_action/<action>/<commission_id>")
    @auth_basic(_auth_check)
    def commission_action(action: str, commission_id: int):
        with Db() as db:
            if action == "claim":
                current_user = db.get_user_from_username(request.auth[0])
                functions.claim_commission(db, commission_id, current_user["id"])
            elif action == "reject":
                functions.reject_commission(db, commission_id)
            elif action == "emailed":
                functions.email_commission(db, commission_id)
            elif action == "remove":
                functions.remove_commission(db, commission_id)
            elif action == "refunded":
                functions.refund_commission(db, commission_id)
            elif action == "archive":
                functions.archive_commission(db, commission_id)
            else:
                abort(400, f"Unknown action: {action}")
        utils.send_to_websockets("commissions")

    @app.post("/finish_commission")
    @auth_basic(_auth_check)
    def finish_commission():
        commission_id = request.forms.commission_id
        image_file = request.files.image_file
        with Db() as db:
            functions.finish_commission(db, commission_id, image_file)
        utils.send_to_websockets("commissions")

    @app.get("/assign_commission/<commission_id>/<user_id>")
    @auth_basic(_auth_check)
    def assign_commission(commission_id: int, user_id: int):
        _assign_commission(commission_id, user_id)

    @app.get("/assign_new_commission/<commission_id>/<user_id>/<num_characters>")
    @auth_basic(_auth_check)
    def assign_new_commission(commission_id: int, user_id: int, num_characters: str):
        _assign_commission(commission_id, user_id, num_characters)

    @app.post("/add_note")
    @auth_basic(_auth_check)
    def add_note():
        commission_id = request.params["commission_id"]
        user_id = request.params["user_id"]
        text = request.params["text"]
        with Db() as db:
            db.add_note(commission_id, user_id, text)
        utils.send_to_websockets("commissions")

    @app.post("/add_new_user")
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
                    new_user_role,
                    request.forms.get("is_artist") == "on",
                    request.forms.get("queue_open") == "on",
                )
            except sqlite3.IntegrityError as e:
                if str(e) == "UNIQUE constraint failed: users.username":
                    abort(400, f"A user with the username '{new_username}' already exists.")
                raise
        utils.send_to_websockets("users")
        t = TEMPLATE_LOOKUP.get_template("redirect_to_main.tpl")
        return t.render(title=f"Added user '{new_username}'", message=f"'{new_username}' has been added to the database.")

    @app.post("/delete_user")
    @auth_basic(_auth_check)
    def delete_user():
        user_id = request.params["user_id"]
        with Db() as db:
            _permissions_check(db, request.auth[0], user_id, allow_change_self=False)
            response = db.delete_user(user_id)
            if response is None:
                abort(400, f"No user found with id={user_id}")
        utils.send_to_websockets("users")
        return f"User with id='{user_id}' has been deleted."

    @app.post("/change_username")
    @auth_basic(_auth_check)
    def change_username():
        user_id = request.params["user_id"]
        username = request.params["new_value"]
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
        utils.send_to_websockets("users")
        if change_self:
            return f"Your username has been changed to '{username}'. " \
                   f"You will need to restart your web browser before you can log back in with your new credentials."
        else:
            return f"User with id='{user_id}' has had their username changed to '{username}'. " \
                   f"The user will need to restart their web browser to log back into the website."

    @app.post("/change_full_name")
    @auth_basic(_auth_check)
    def change_full_name():
        user_id = request.params["user_id"]
        full_name = request.params["new_value"]
        with Db() as db:
            change_self = _permissions_check(db, request.auth[0], user_id)
            if not full_name:
                abort(400, f"{full_name} is not a valid name.")
            response = db.change_full_name(user_id, full_name)
            if response is None:
                abort(400, f"No user found with id={user_id}")
        utils.send_to_websockets("users")
        if change_self:
            return f"Your name has been changed to '{full_name}'."
        else:
            return f"User with id='{user_id}' has had their full name changed to '{full_name}'."

    @app.post("/change_password")
    @auth_basic(_auth_check)
    def change_password():
        user_id = request.params["user_id"]
        password = request.params["new_value"]
        with Db() as db:
            change_self = _permissions_check(db, request.auth[0], user_id)
            if not password:
                abort(400, f"{password} is not a valid password.")
            response = db.change_password(user_id, bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
            if response is None:
                abort(400, f"No user found with id={user_id}")
                return
            username = db.get_username_from_id(user_id)
        _delete_from_password_cache(username)
        if change_self:
            return "Your password has been changed. " \
                   "You will need to restart your web browser before you can log back in with your new credentials."
        else:
            return f"User with id='{user_id}' has had their password changed. " \
                   f"The user will need to restart their web browser to log back into the website."

    @app.post("/change_is_artist")
    @auth_basic(_auth_check)
    def change_is_artist():
        user_id = request.params["user_id"]
        is_artist = request.params["is_artist"]
        is_artist = is_artist.lower() == "true"
        with Db() as db:
            _permissions_check(db, request.auth[0], user_id, allow_change_self=False)
            response = db.change_is_artist(user_id, is_artist)
            if response is None:
                abort(400, f"No user found with id={user_id}")
                return
        utils.send_to_websockets("users")

    @app.post("/change_queue_open")
    @auth_basic(_auth_check)
    def change_queue_open():
        user_id = request.params["user_id"]
        queue_open = request.params["queue_open"]
        queue_open = queue_open.lower() == "true"
        with Db() as db:
            _permissions_check(db, request.auth[0], user_id)
            response = db.change_queue_open(user_id, queue_open)
            if response is None:
                abort(400, f"No user found with id={user_id}")
                return
        utils.send_to_websockets("refresh")

    @app.error(401)
    def invalid_user(*args):
        if request.auth is not None:
            _delete_from_password_cache(request.auth[0])
        t = TEMPLATE_LOOKUP.get_template("error_401.tpl")
        return t.render()

    @app.post("/kofi_webhook")
    def kofi_webhook():
        if not request.params or "data" not in request.params:
            print(f"Invalid request: {dict(request.params)}", file=sys.stderr)
            abort(400)
            return
        print(request.params)
        try:
            data = loads(request.params["data"])
        except Exception:
            print(f"Not valid JSON: {request.params['data']}", file=sys.stderr)
            abort(400)
            return
        if data.get("verification_token") != os.environ["KOFI_VERIFICATION_TOKEN"]:
            print(f"Incorrect verification token: {data}", file=sys.stderr)
            abort(403)
            return
        if data.get("type") != "Commission":
            log = f"Received non-commission data. Skipping. {data}"
            print(log)
        else:
            log = f"New Ko-fi commission! {data}"
            print(log)
            functions.add_commission(data)
            utils.send_to_websockets("commissions")
        try:
            with open("audit.log", "a") as f:
                f.write(log + "\r\n")
        except Exception as e:
            print(e, file=sys.stderr)


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
        abort(403, "Sorry, only admins can perform that action.")
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


def _get_users(db: Db, current_user: dict) -> List[dict]:
    if not current_user["role"] in ["god", "admin"]:
        return []
    # Sort users by role
    users = sorted(list(db.get_users()), key=lambda u: ({"god": 0, "admin": 1, "user": 2}[u["role"]], u["id"]))
    # Determine if user buttons should be enabled or disabled for each user
    for user in users:
        if user["role"] == "god":
            user["disable_user_buttons"] = True
        elif user["role"] == "admin":
            user["disable_user_buttons"] = current_user["role"] != "god"
        else:
            user["disable_user_buttons"] = False
    return users


def _get_notes(db: Db, commission_ids: List[int]):
    notes = db.get_notes(commission_ids)
    notes_dict = defaultdict(list)
    for note in notes:
        # Convert to markdown and strip post paragraph tag
        note["text"] = MD.convert(note["text"])[:-5]
        notes_dict[note["commission_id"]].append(note)
    return notes_dict


def _fetch_commissions(db: Db, current_user: dict, opened_commissions: List[str], hidden_queues: List[str]) -> Dict[str, dict]:
    my_commissions = {"hidden": "my_commissions" in hidden_queues, "commissions": []}
    new_commissions = {"hidden": "new_commissions" in hidden_queues, "commissions": []}
    available_commissions = {"hidden": "available_commissions" in hidden_queues, "commissions": []}
    other_commissions = {}
    finished_commissions = {"hidden": "finished_commissions" in hidden_queues, "commissions": []}
    removed_commissions = {"hidden": "removed_commissions" in hidden_queues, "commissions": []}
    # Build user-specific commission queues
    for user in db.get_all_artists():
        other_commissions[user["username"]] = {
            "user": user,
            "hidden": user["username"] in hidden_queues,
            "commissions": []
        }
    # Get commission notes
    commissions = list(db.get_all_commissions_with_users())
    commission_ids = [c["id"] for c in commissions]
    notes_dict = _get_notes(db, commission_ids)
    # Organize commissions into queues
    time_offset = 8 * 3600
    for commission in commissions:
        # Modify data
        if str(commission["id"]) in opened_commissions:
            commission["open"] = True
        if commission["assigned_to"] == -1:
            commission["assigned_string"] = "Unassigned"
        else:
            commission["assigned_string"] = "Assigned to {}".format(commission["full_name"])
        commission["status"], commission["status_text"] = utils.get_status(commission)
        commission["created_epoch"] = int(mktime(strptime(commission["created_ts"], "%Y-%m-%dT%H:%M:%SZ"))) - time_offset
        commission["updated_epoch"] = int(mktime(strptime(commission["updated_ts"], "%Y-%m-%d %H:%M:%S"))) - time_offset
        commission["notes"] = notes_dict.get(commission["id"], [])
        # Assign to queue
        if commission["status"] == "new_status":
            new_commissions["commissions"].append(commission)
        elif commission["status"] == "claimable_status":
            available_commissions["commissions"].append(commission)
        elif commission["status"] in ("finished_status", "emailed_status"):
            finished_commissions["commissions"].append(commission)
        elif commission["status"] in ("removed_status", "refunded_status"):
            removed_commissions["commissions"].append(commission)
        else:
            # In an Artist's commission queue
            if commission["assigned_to"] == current_user["id"]:
                my_commissions["commissions"].append(commission)
            else:
                other_commissions[commission["username"]]["commissions"].append(commission)
    # Sort commissions
    def sort_key(d):
        return d["updated_epoch"], d["created_epoch"], d["id"]
    my_commissions["commissions"] = sorted(my_commissions["commissions"], key=sort_key)
    new_commissions["commissions"] = sorted(new_commissions["commissions"], key=sort_key)
    available_commissions["commissions"] = sorted(available_commissions["commissions"], key=sort_key)
    for d in other_commissions.values():
        d["commissions"] = sorted(d["commissions"], key=sort_key)
    finished_commissions["commissions"] = sorted(finished_commissions["commissions"], key=sort_key)
    return {
        "my_commissions": my_commissions,
        "new_commissions": new_commissions,
        "available_commissions": available_commissions,
        "other_commissions": other_commissions,
        "finished_commissions": finished_commissions,
        "removed_commissions": removed_commissions,
    }


def _assign_commission(commission_id: int, user_id: int, num_characters: str=None):
    with Db() as db:
        _permissions_check(db, request.auth[0])
        commission = db.get_commission_by_id(commission_id)
        if commission["preferred_artist"] is None:
            if user_id == "-1":
                db.set_preferred_artist(commission_id, "Any", False)
            else:
                artist_name = db.get_full_name_from_id(user_id)
                db.set_preferred_artist(commission_id, artist_name, True)
        if num_characters is not None:
            db.set_num_characters(commission_id, num_characters)
        functions.assign_commission(db, commission_id, user_id)
        utils.send_to_websockets("commissions")
