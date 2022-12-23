import os
import re
import sys
from typing import Optional, Dict, Union

import bottle
from src.db.db import Db


# def update_commissions_information(randomize=False):
#     print("")
#     print(ctime())
#     rows = get_standard_commissions()
#     if randomize:
#         shuffle(rows)
#     needs_update = False
#     with Db() as db:
#         for row in rows:
#             if add_commission(db, row):
#                 needs_update = True
#     print("Done processing new commissions")
#     return needs_update


# def add_commission(db: Db, row: list) -> Optional[dict]:
#     del row[1]  # Delete TOS agreement
#     if len(row) < 13:
#         row.append("")
#     if db.get_commission_by_email(row[0], row[2]):
#         return None
#     print(f"Adding commission... {row}")
#     commission = db.add_commission(row)
#     if commission is None:
#         # Commission was already added to the table, so skip it
#         return None
#     # Assign the commission to someone based on artist_choice
#     assigned_to = -1
#     if not commission["artist_choice"].startswith("Any artist"):
#         user_id = db.get_user_id_from_full_name(commission["artist_choice"])
#         if user_id is None:
#             print(f"No user found with full name '{commission['artist_choice']}'", file=sys.stderr)
#         else:
#             assigned_to = user_id
#     commission = db.assign_commission(commission["id"], assigned_to)
#     # Set allow_any_artist flag
#     allow_any_artist = (
#         not commission.get("if_queue_is_full") or
#         "any artist" in (commission.get("if_queue_is_full") or "").lower()
#     )
#     commission = db.set_allow_any_artist(commission["id"], allow_any_artist)
#     db.conn.commit()
#     return commission


def add_commission(data: Dict[str, Union[str, bool, None]]) -> Optional[dict]:
    with Db() as db:
        print(f"Adding commission... {data}")
        commission = db.add_commission(
            data["timestamp"],
            data["from_name"],
            data["email"],
            data["amount"],
            data["message"],
            data["url"],
        )
        if commission is None:
            # Commission was already added to the table, so skip it
            print(f"Duplicate commission: {data}")
            return None
        db.conn.commit()
    return commission


# def get_standard_commissions():
#     return get_commissions_info_from_spreadsheet("Form Responses 1!A2:N")
#
#
# def get_special_commissions():
#     commissions_list = get_commissions_info_from_spreadsheet("Form Responses 2!A2:M")
#     for commission in commissions_list:
#         commission[-3] = commission[-3].split(" (")[0]
#         commission[-2] = "Specialty request"
#     return commissions_list


# def get_commissions_info_from_spreadsheet(sheet_range) -> List:
#     print("Loading Google Sheet of commission info...")
#     service = build('sheets', 'v4', developerKey=os.environ["GOOGLE_SHEETS_DEVELOPER_KEY"])
#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     thing = sheet.values().get(spreadsheetId=os.environ["SPREADSHEET_ID"], range=sheet_range)
#     result = thing.execute()["values"]
#     print(f"Got {len(result)} results")
#     return result


def assign_commission(db: Db, commission_id: int, user_id: int) -> Optional[dict]:
    db.assign_commission(commission_id, user_id)
    db.unfinish_commission(commission_id)
    db.remove_commission(commission_id, False)
    return db.update_ts(commission_id)


def claim_commission(db: Db, commission_id: int, user_id: int) -> Optional[dict]:
    return assign_commission(db, commission_id, user_id)


def approve_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.set_preferred_artist(commission_id, "Any", False)
    db.assign_commission(commission_id, -1)
    return db.update_ts(commission_id)


def reject_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.assign_commission(commission_id, -1)
    return db.update_ts(commission_id)


def finish_commission(db: Db, commission_id: int, image_file: bottle.FileUpload) -> Optional[dict]:
    commission = db.get_commission_by_id(commission_id)
    commissioner_name = re.sub(r"\W", "_", commission["name"].lower())
    assigned_artist = db.get_username_from_id(commission["assigned_to"])
    try:
        _, ext = os.path.splitext(image_file.filename)
    except Exception:
        print(image_file, file=sys.stderr)
        raise
    os.makedirs("finished_commissions", exist_ok=True)
    filename = f"{commission['id']:>02}_{commissioner_name}_by_{assigned_artist}{ext}"
    filepath = f"finished_commissions/{filename}"
    i = 0
    while os.path.isfile(filepath):
        i += 1
        filename = f"{commission['id']:>02}_{commissioner_name}_by_{assigned_artist}_{i}{ext}"
        filepath = f"finished_commissions/{filename}"
    image_file.save(filepath)
    db.finish_commission(commission_id, filename)
    # db.assign_commission(commission_id, -1)
    return db.update_ts(commission_id)


def email_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.email_commission(commission_id)
    return db.update_ts(commission_id)


def remove_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.remove_commission(commission_id)
    return db.update_ts(commission_id)


def refund_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.refund_commission(commission_id)
    return db.update_ts(commission_id)


def archive_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.archive_commission(commission_id)
    return db.update_ts(commission_id)


def generate_commissions_text_file(db: Db):
    day_of = "Sun"
    shared_folder = r"\\marmalade\Users\artis\Desktop"
    commissions = db.get_all_commissions()
    filtered_commissions = [c for c in commissions if c["assigned_to"] in (-1, 2) and
                            not c["finished"] and not c["removed"] and not c["archived"] and
                            c["num_characters"] and c["num_characters"].startswith(day_of)]
    def sort_key(d):
        return d["assigned_to"] == -1, d["created_ts"]
    sorted_commissions = sorted(filtered_commissions, key=sort_key)
    def print_queue(commission_type, commissions):
        filtered_commissions = [c for c in commissions if commission_type in c["num_characters"]]
        n = 4  # Number of commissions to show
        s = ""
        # s = f"{commission_type} Commission Queue:\n"
        for c in filtered_commissions[:n]:
            s += f" - {c['name']}"
            if c["assigned_to"] == 2:
                s += " (in progress)"
            s += "\n"
        if len(filtered_commissions) > n:
            s += f"({len(filtered_commissions) - n} more)"
        return s
    with open(os.path.join(shared_folder, "sketch_queue.txt"), "w") as f:
        f.write(print_queue("Sketch", sorted_commissions))
    with open(os.path.join(shared_folder, "doodle_queue.txt"), "w") as f:
        f.write(print_queue("Doodle", sorted_commissions))


if __name__ == "__main__":
    os.chdir("..")
    # update_commissions_information()
    with Db() as db:
        generate_commissions_text_file(db)
