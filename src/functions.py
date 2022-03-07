import os
import sys
from random import shuffle
from typing import Optional, List

from googleapiclient.discovery import build

from src.db.db import Db

GOOGLE_SHEETS_DEVELOPER_KEY = os.environ["GOOGLE_SHEETS_DEVELOPER_KEY"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]


def __init__():
    with Db() as db:
        db.check_version()


def send_status_update(action_name: str, commission_id: id, user_name: str, channel_name: str):
    print(
        "Commission #{} has been {} by {} in channel {}".format(
            commission_id,
            action_name,
            user_name,
            channel_name
        )
    )


def update_commissions_information(randomize=False):
    rows = get_standard_commissions()
    if randomize:
        shuffle(rows)
    with Db() as db:
        for row in rows:
            add_commission(db, row)
    print("Done processing new commissions")


def add_commission(db: Db, row: list) -> Optional[dict]:
    del row[1]  # Delete TOS agreement
    if len(row) < 13:
        row.append("")
    commission = db.add_commission(row)
    if commission is None:
        # Commission was already added to the table, so skip it
        return
    # Assign the commission to someone based on artist_choice
    assigned_to = -1
    if not commission["artist_choice"].startswith("Any artist"):
        user_id = db.get_user_id_from_full_name(commission["artist_choice"])
        if user_id is None:
            print(f"No user found with full name '{commission['artist_choice']}'", file=sys.stderr)
        else:
            assigned_to = user_id
    commission = db.assign_commission(commission["id"], assigned_to)
    # Set allow_any_artist flag
    allow_any_artist = (
        not commission.get("if_queue_is_full") or
        "any artist" in (commission.get("if_queue_is_full") or "").lower()
    )
    db.set_allow_any_artist(commission["id"], allow_any_artist)
    db.conn.commit()


def get_standard_commissions():
    return get_commissions_info_from_spreadsheet("Form Responses 1!A2:N")


def get_special_commissions():
    commissions_list = get_commissions_info_from_spreadsheet("Form Responses 2!A2:M")
    for commission in commissions_list:
        commission[-3] = commission[-3].split(" (")[0]
        commission[-2] = "Specialty request"
    return commissions_list


def get_commissions_info_from_spreadsheet(sheet_range) -> List:
    print("Loading Google Sheet of commission info...")
    service = build('sheets', 'v4', developerKey=GOOGLE_SHEETS_DEVELOPER_KEY)
    # Call the Sheets API
    sheet = service.spreadsheets()
    thing = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=sheet_range)
    result = thing.execute()["values"]
    print(f"Got {len(result)} results")
    return result


def claim_commission(user_id: int, commission_id: int) -> Optional[dict]:
    with Db() as db:
        commission = db.get_commission_by_id(commission_id)
        # The commission must not currently be assigned to anyone to allow a claim
        if commission["assigned_to"] is not None:
            print(f"A user (id={user_id}) tried to claim a commission that was already claimed. How??")
            raise Exception(
                f"You tried to claim a commission that was already claimed. Please tell Trick-Candle how."
            )
        # If the commission is exclusive and in the voided-queue, claim will give it back to the original
        # requested artist
        if not commission["allow_any_artist"] and commission["channel_name"] == "voided-queue":
            name = commission["artist_choice"]
            auto_accept = False
        else:
            # If the commission is limited to a specific artist, the claiming artist must be that artist
            if not commission["allow_any_artist"] and commission["artist_choice_id"] != user_id:
                return None
            auto_accept = True
        commission = db.assign_commission(name, message_id=commission_id)
        if auto_accept:
            commission = db.accept_commission(commission_id, accepted=True)
        return commission


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


def reject_commission(commission_id: int) -> bool:
    with Db() as db:
        db.assign_commission(None, message_id=commission_id)
        commission = db.accept_commission(commission_id, accepted=False)
        return commission


def accept_commission(user_id: int, commission_id: int) -> Optional[dict]:
    with Db() as db:
        return db.accept_commission(commission_id, accepted=True)


def invoice_commission(message_id: int) -> dict:
    with Db() as db:
        return db.invoice_commission(message_id)


def pay_commission(message_id: int) -> dict:
    with Db() as db:
        return db.pay_commission(message_id)


def finish_commission(message_id: int) -> dict:
    with Db() as db:
        db.finish_commission(message_id)
        return db.hide_commission(message_id, hidden=True)


if __name__ == "__main__":
    os.chdir("..")
    update_commissions_information()
