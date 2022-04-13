import os.path
import sqlite3
from collections import OrderedDict
from typing import Optional, Iterator, Union

DB_CONN = None
VERSION_NEEDED = 1


class Db:

    def __init__(self, filename="database_files/main.db", auto_commit=True, auto_close=True):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"No DB found at {os.path.join(os.getcwd(), filename)}")
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
        self.check_version()
        self.auto_commit = auto_commit
        self.auto_close = auto_close

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
                if self.auto_close:
                    self.close()

    def close(self):
        if self.conn:
            self.conn.close()

    def _row_to_dict(self, row) -> dict:
        d = OrderedDict()
        for i, col in enumerate(self.cur.description):
            d[col[0]] = row[i]
        return d

    def _scalar(self, sql, params) -> Union[str, int, bool, None]:
        result = self.cur.execute(sql, params).fetchone()
        if result is None:
            return None
        return result[0]

    def _fetch_one(self, sql, params) -> Optional[dict]:
        result = self.cur.execute(sql, params).fetchone()
        if result is None:
            return None
        return self._row_to_dict(result)

    def _yield_dicts(self, sql, params=None) -> Iterator[dict]:
        if params is None:
            ex = self.cur.execute(sql)
        else:
            ex = self.cur.execute(sql, params)
        for row in ex.fetchall():
            yield self._row_to_dict(row)

    def check_version(self):
        sql = "SELECT version FROM version;"
        version = self.cur.execute(sql).fetchone()[0]
        if not version == VERSION_NEEDED:
            raise ValueError(f"Incorrect DB version: {version} != {VERSION_NEEDED}")

    # USER MANAGEMENT

    def set_god_user(self, username: str, full_name: str, password_hash: bytes):
        sql = """
            SELECT * FROM users WHERE role='god';
        """
        god_users = list(self.cur.execute(sql))
        if len(god_users) == 0:
            sql = """
                INSERT INTO users(username, full_name, password_hash, role) VALUES (?, ?, ?, 'god');
            """
            self.cur.execute(sql, [username, full_name, password_hash])
        elif len(god_users) == 1:
            sql = """
                UPDATE users SET username=?, full_name=?, password_hash=? WHERE role='god';
            """
            self.cur.execute(sql, [username, full_name, password_hash])
        else:
            raise ValueError(f"{len(god_users)} god users found. "
                             f"Something fucky is going on, please audit users in DB.")

    def add_user(self, username: str, full_name: str, password_hash: bytes, role: str="user", is_artist: bool=True):
        if role not in ["admin", "user"]:
            raise ValueError("role must be either 'admin' or 'user'")
        sql = """
            INSERT INTO users(username, full_name, password_hash, role, is_artist) VALUES (?, ?, ?, ?, ?);
        """
        self.cur.execute(sql, [username, full_name, password_hash, role, is_artist])

    def delete_user(self, user_id: int):
        sql = """
            DELETE FROM users WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [user_id])

    def change_username(self, user_id: int, username: str):
        sql = """
            UPDATE users SET username=? WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [username, user_id])

    def change_full_name(self, user_id: int, full_name: str):
        sql = """
            UPDATE users SET full_name=? WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [full_name, user_id])

    def change_password(self, user_id: int, password_hash: bytes):
        sql = """
            UPDATE users SET password_hash=? WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [password_hash, user_id])

    def change_role(self, user_id: int, role: str):
        if role not in ["admin", "user"]:
            raise ValueError("role must be either 'admin' or 'user'")
        sql = """
            UPDATE users SET role=? WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [role, user_id])

    def change_is_artist(self, user_id: int, is_artist: bool):
        sql = """
            UPDATE users SET is_artist=? WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [is_artist, user_id])

    def get_users(self) -> Iterator[dict]:
        sql = """
            SELECT id, username, full_name, role, is_artist FROM users WHERE NOT role='system'; 
        """
        return self._yield_dicts(sql)

    def get_password_hash_for_username(self, username: str) -> Optional[str]:
        sql = """
            SELECT password_hash FROM users WHERE username=?;
        """
        return self._scalar(sql, [username])

    def get_user_from_username(self, username: str) -> Optional[dict]:
        sql = """
            SELECT id, username, full_name, role, is_artist FROM users WHERE username=?;
        """
        return self._fetch_one(sql, [username])

    def get_user_role_from_username(self, username: str) -> Optional[str]:
        sql = """
            SELECT role FROM users WHERE username=? AND NOT role='system';
        """
        return self._scalar(sql, [username])

    def get_user_id_from_full_name(self, full_name: str) -> Optional[int]:
        sql = """
            SELECT id FROM users WHERE full_name=? AND NOT role='system';
        """
        return self._scalar(sql, [full_name])

    def get_username_from_id(self, user_id: int) -> Optional[str]:
        sql = """
            SELECT username FROM users WHERE id=? AND NOT role='system';
        """
        return self._scalar(sql, [user_id])

    def get_user_role_from_id(self, user_id: int) -> Optional[str]:
        sql = """
            SELECT role FROM users WHERE id=? AND NOT role='system';
        """
        return self._scalar(sql, [user_id])

    # COMMISSIONS

    def get_all_commissions(self) -> Iterator[dict]:
        sql = """
            SELECT * FROM commissions;
        """
        return self._yield_dicts(sql)

    def get_all_commissions_with_users(self) -> Iterator[dict]:
        sql = """
            SELECT 
                c.*,
                u.username,
                u.full_name
            FROM commissions c
            INNER JOIN users u ON c.assigned_to = u.id;
        """
        return self._yield_dicts(sql)

    def get_all_commissions_for_user(self, user_id: str) -> Iterator[dict]:
        sql = """
            SELECT * FROM commissions WHERE assigned_to=?;
        """
        return self._yield_dicts(sql, [user_id])

    def add_commission(self, row) -> dict:
        sql = """
        INSERT INTO commissions(timestamp, name, email, twitch, twitter, discord, num_characters,
            reference_images, description, expression, notes, artist_choice, if_queue_is_full)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING *;
        """
        values = row.copy()
        # print(f"Adding to DB: {values}")
        return self._fetch_one(sql, values)

    def get_commission_by_email(self, timestamp: str, email: str) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE timestamp=? AND email=?;
        """
        return self._fetch_one(sql, [timestamp, email])

    def get_commission_by_id(self, commission_id: int) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE id=?;
        """
        return self._fetch_one(sql, [commission_id])

    def assign_commission(self, commission_id: int, assigned_to: int) -> dict:
        sql = "UPDATE commissions SET assigned_to=? WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [assigned_to, commission_id])

    def set_allow_any_artist(self, commission_id: int, allow_any_artist: bool) -> dict:
        sql = "UPDATE commissions SET allow_any_artist=? WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [allow_any_artist, commission_id])

    def accept_commission(self, commission_id: int, accepted=True):
        sql = "UPDATE commissions SET accepted=? WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [accepted, commission_id])

    def invoice_commission(self, commission_id: int, invoiced=True):
        sql = "UPDATE commissions SET invoiced=? WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [invoiced, commission_id])

    def pay_commission(self, commission_id: int, paid=True):
        sql = "UPDATE commissions SET paid=? WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [paid, commission_id])

    def finish_commission(self, commission_id: int, finished=True):
        sql = "UPDATE commissions SET finished=? WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [finished, commission_id])
