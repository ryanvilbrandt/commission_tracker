import os.path
import sqlite3
from collections import OrderedDict
from typing import List, Optional

VERSION_NEEDED = 1


class Db:

    def __init__(self, filename="database_files/main.db", auto_commit=True):
        if not os.path.isfile(filename):
            raise FileNotFoundError
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.check_version()
        self.auto_commit = auto_commit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                if exc_type:
                    self.conn.rollback()
                elif self.auto_commit:
                    self.conn.commit()
            finally:
                self.close()

    def close(self):
        if self.conn:
            self.conn.close()

    def row_to_dict(self, row):
        d = OrderedDict()
        for i, col in enumerate(self.cur.description):
            d[col[0]] = row[i]
        return d

    def fetch_dict(self, sql, params):
        result = self.cur.execute(sql, params).fetchone()
        if result is None:
            return None
        return self.row_to_dict(result)

    def check_version(self):
        sql = "SELECT version FROM version;"
        version = self.cur.execute(sql).fetchone()[0]
        if not version == VERSION_NEEDED:
            raise ValueError(f"Incorrect DB version: {version} != {VERSION_NEEDED}")

    def set_god_user(self, username, password_hash):
        sql = """
            SELECT * FROM users WHERE role='god';
        """
        god_users = list(self.cur.execute(sql))
        if len(god_users) == 0:
            sql = """
                INSERT INTO users(username, password_hash, role) VALUES (?, ?, 'god');
            """
            self.cur.execute(sql, [username, password_hash])
        elif len(god_users) == 1:
            sql = """
                UPDATE users SET username=?, password_hash=?;
            """
            self.cur.execute(sql, [username, password_hash])
        else:
            raise ValueError(f"{len(god_users)} god users found. Something fucky is going on, please audit users in DB.")

    def add_user(self, username, password_hash, role="user"):
        if role not in ["admin", "user"]:
            raise ValueError("role must be either 'admin' or 'user'")
        sql = """
            INSERT INTO users(username, password_hash, role) VALUES (?, ?, ?);
        """
        self.cur.execute(sql, [username, password_hash, role])

    def change_username(self, user_id, username):
        sql = """
            UPDATE users SET username=? WHERE id=? AND NOT role='god';
        """
        self.cur.execute(sql, [username, user_id])

    def change_password(self, user_id, password_hash):
        sql = """
            UPDATE users SET password_hash=? WHERE id=? AND NOT role='god';
        """
        self.cur.execute(sql, [password_hash, user_id])

    def change_role(self, user_id, role):
        if role not in ["admin", "user"]:
            raise ValueError("role must be either 'admin' or 'user'")
        sql = """
            UPDATE users SET role=? WHERE id=?;
        """
        self.cur.execute(sql, [role, user_id])

    def get_all_commissions(self) -> List[dict]:
        sql = """
            SELECT * FROM commissions;
        """
        for row in self.cur.execute(sql).fetchall():
            yield self.row_to_dict(row)

    def get_all_commissions_for_queue(self, channel_name: str) -> List[dict]:
        sql = """
            SELECT * FROM commissions WHERE channel_name=?;
        """
        for row in self.cur.execute(sql, [channel_name]).fetchall():
            yield self.row_to_dict(row)

    def add_commission(self, row) -> dict:
        sql = """
        INSERT INTO commissions(timestamp, email, twitch, twitter, discord, 
            reference_images, description, expression, notes, artist_choice, if_queue_is_full, name) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING *;
        """
        values = row.copy()
        # print(f"Adding to DB: {values}")
        return self.fetch_dict(sql, values)

    def get_commission_by_email(self, timestamp: str, email: str) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE timestamp=? AND email=?;
        """
        return self.fetch_dict(sql, [timestamp, email])

    def get_commission_by_message_id(self, message_id: int) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE message_id=?;
        """
        return self.fetch_dict(sql, [message_id])

    def get_commission_by_id(self, db_id: int) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE id=?;
        """
        return self.fetch_dict(sql, [db_id])

    def increment_channel_counter(self, channel_name: str) -> int:
        sql = """
            UPDATE channels SET counter=counter + 1 WHERE channel_name=? RETURNING counter;
        """
        return self.cur.execute(sql, [channel_name]).fetchone()[0]

    def update_commission_counter(self, timestamp: str, email: str, counter: int):
        sql = """
            UPDATE commissions SET counter=? WHERE timestamp=? AND email=? RETURNING *;
        """
        return self.fetch_dict(sql, [counter, timestamp, email])

    def update_message_id(self, timestamp: str, email: str, channel_name: str, message_id: int) -> dict:
        sql = """
            UPDATE commissions SET channel_name=?, message_id=? WHERE timestamp=? AND email=? RETURNING *;
        """
        return self.fetch_dict(sql, [channel_name, message_id, timestamp, email])

    def assign_commission(self, assigned_to: Optional[str], timestamp: str=None, email: str=None,
                          message_id: int=None) -> dict:
        if timestamp and email:
            sql = "UPDATE commissions SET assigned_to=? WHERE timestamp=? AND email=? RETURNING *;"
            params = [assigned_to, timestamp, email]
        elif message_id:
            sql = "UPDATE commissions SET assigned_to=? WHERE message_id=? RETURNING *;"
            params = [assigned_to, message_id]
        else:
            raise ValueError("Either message_id or (timestamp and email) must be set.")
        return self.fetch_dict(sql, params)

    def set_allow_any_artist(self, allow_any_artist: bool, timestamp: str=None, email: str=None) -> dict:
        sql = "UPDATE commissions SET allow_any_artist=? WHERE timestamp=? AND email=? RETURNING *;"
        params = [allow_any_artist, timestamp, email]
        return self.fetch_dict(sql, params)

    def set_specialty(self, specialty: bool, timestamp: str=None, email: str=None) -> dict:
        sql = "UPDATE commissions SET specialty=? WHERE timestamp=? AND email=? RETURNING *;"
        params = [specialty, timestamp, email]
        return self.fetch_dict(sql, params)

    def accept_commission(self, message_id: int, accepted=True):
        sql = """
            UPDATE commissions SET accepted=? WHERE message_id=? RETURNING *; 
        """
        return self.fetch_dict(sql, [accepted, message_id])

    def hide_commission(self, message_id: int, hidden):
        sql = """
            UPDATE commissions SET hidden=? WHERE message_id=? RETURNING *; 
        """
        return self.fetch_dict(sql, [hidden, message_id])

    def invoice_commission(self, message_id: int, invoiced=True):
        sql = """
            UPDATE commissions SET invoiced=? WHERE message_id=? RETURNING *; 
        """
        return self.fetch_dict(sql, [invoiced, message_id])

    def pay_commission(self, message_id: int, paid=True):
        sql = """
            UPDATE commissions SET paid=? WHERE message_id=? RETURNING *; 
        """
        return self.fetch_dict(sql, [paid, message_id])

    def finish_commission(self, message_id: int, finished=True):
        sql = """
            UPDATE commissions SET finished=? WHERE message_id=? RETURNING *; 
        """
        return self.fetch_dict(sql, [finished, message_id])

#
# if __name__ == "__main__":
#     with Db(filename="../../database_files/main.db") as db:
#         db.cur.execute("DELETE FROM commissions;")
