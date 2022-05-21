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
    db.unfinish_commission(commission_id)
    db.accept_commission(commission_id, False)
    db.assign_commission(commission_id, user_id)
    return db.update_ts(commission_id)


def claim_commission(db: Db, user_id: int, commission_id: int) -> Optional[dict]:
    # commission = db.get_commission_by_id(commission_id)
    # The commission must not currently be assigned to anyone to allow a claim
    # if commission["assigned_to"] != -1:
    #     print(f"A user (id={user_id}) tried to claim a commission that was already claimed. How??")
    #     raise Exception(
    #         f"You tried to claim a commission that was already claimed. Please tell Trick-Candle how."
    #     )
    # # If the commission is exclusive and in the voided-queue, claim will give it back to the original
    # # requested artist
    # if not commission["allow_any_artist"] and commission["channel_name"] == "voided-queue":
    #     name = commission["artist_choice"]
    #     auto_accept = False
    # else:
    #     # If the commission is limited to a specific artist, the claiming artist must be that artist
    #     if not commission["allow_any_artist"] and commission["artist_choice_id"] != user_id:
    #         return None
    #     auto_accept = True
    db.assign_commission(commission_id, user_id)
    # if auto_accept:
    db.accept_commission(commission_id, accepted=True)
    db.unfinish_commission(commission_id)
    return db.update_ts(commission_id)


# @staticmethod
# def check_if_user_can_accept_reject(db: Db, member: Member, message_id: int, action: str):
#     commission = db.get_commission_by_message_id(message_id)
#     name = get_name_by_member_id(member.id)
#     if name != commission["assigned_to"]:
#         print(f"A user ({member} | {name}) tried to {action} a commission "
#               f"when it wasn't assigned to them ({commission['assigned_to']}).")
#         member.send(f"You can't {action} a commission that isn't assigned to you.", delete_after=60)
#         return None
#     return commission


def accept_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.accept_commission(commission_id, accepted=True)
    return db.update_ts(commission_id)


def reject_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.accept_commission(commission_id, accepted=False)
    db.assign_commission(commission_id, -1)
    return db.update_ts(commission_id)


def invoice_commission(db: Db, commission_id: int, invoiced: bool=True) -> Optional[dict]:
    db.invoice_commission(commission_id, invoiced=invoiced)
    return db.update_ts(commission_id)


def pay_commission(db: Db, commission_id: int, paid: bool=True) -> Optional[dict]:
    db.pay_commission(commission_id, paid=paid)
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


def archive_commission(db: Db, commission_id: int) -> Optional[dict]:
    db.archive_commission(commission_id)
    return db.update_ts(commission_id)


if __name__ == "__main__":
    os.chdir("..")
    # update_commissions_information()
