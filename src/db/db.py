import os.path
import sqlite3
from collections import OrderedDict
from typing import Optional, Iterator, Union

DB_CONN = None


class Db:

    def __init__(self, filename="database_files/main.db", auto_commit=True, auto_close=True):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"No DB found at {os.path.join(os.getcwd(), filename)}")
        self.conn = sqlite3.connect(filename)
        self.cur = self.conn.cursor()
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

    def _fetch_all(self, sql, params=None) -> Iterator[dict]:
        if params is None:
            ex = self.cur.execute(sql)
        else:
            ex = self.cur.execute(sql, params)
        for row in ex.fetchall():
            yield self._row_to_dict(row)

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

    def add_user(self, username: str, full_name: str, password_hash: bytes, role: str="user", is_artist: bool=True,
                 queue_open: bool=True):
        if role not in ["admin", "user"]:
            raise ValueError("role must be either 'admin' or 'user'")
        sql = """
            INSERT INTO users(username, full_name, password_hash, role, is_artist, queue_open) 
            VALUES (?, ?, ?, ?, ?, ?);
        """
        self.cur.execute(sql, [username, full_name, password_hash, role, is_artist, queue_open])

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

    def change_queue_open(self, user_id: int, queue_open: bool):
        sql = """
            UPDATE users SET queue_open=? WHERE id=? AND NOT role='god' AND NOT role='system' RETURNING id;
        """
        return self._scalar(sql, [queue_open, user_id])

    def get_users(self) -> Iterator[dict]:
        sql = """
            SELECT id, username, full_name, role, is_artist, queue_open FROM users WHERE NOT role='system'; 
        """
        return self._fetch_all(sql)

    def get_password_hash_for_username(self, username: str) -> Optional[str]:
        sql = """
            SELECT password_hash FROM users WHERE username=?;
        """
        return self._scalar(sql, [username])

    def get_user_from_username(self, username: str) -> Optional[dict]:
        sql = """
            SELECT id, username, full_name, role, is_artist, queue_open FROM users WHERE username=?;
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

    def get_full_name_from_id(self, user_id: int) -> Optional[str]:
        sql = """
            SELECT full_name FROM users WHERE id=? AND NOT role='system';
        """
        return self._scalar(sql, [user_id])

    def get_user_role_from_id(self, user_id: int) -> Optional[str]:
        sql = """
            SELECT role FROM users WHERE id=? AND NOT role='system';
        """
        return self._scalar(sql, [user_id])

    def get_all_artists(self) -> Iterator[dict]:
        sql = """
            SELECT username, full_name, queue_open FROM users WHERE is_artist=TRUE;
        """
        return self._fetch_all(sql)

    # COMMISSIONS

    def get_all_commissions(self) -> Iterator[dict]:
        sql = """
            SELECT * FROM commissions;
        """
        return self._fetch_all(sql)

    def get_all_commissions_with_users(self) -> Iterator[dict]:
        sql = """
            SELECT 
                c.*,
                u.username,
                u.full_name
            FROM commissions c
            INNER JOIN users u ON c.assigned_to = u.id;
        """
        return self._fetch_all(sql)

    def get_all_commissions_for_user(self, user_id: str) -> Iterator[dict]:
        sql = """
            SELECT * FROM commissions WHERE assigned_to=?;
        """
        return self._fetch_all(sql, [user_id])

    def add_commission(self, created_ts, name, email, price, message, url) -> dict:
        sql = """
        INSERT INTO commissions(created_ts, name, email, price, message, url)
        VALUES (?, ?, ?, ?, ?, ?)
        RETURNING *;
        """
        return self._fetch_one(sql, [created_ts, name, email, price, message, url])

    def get_commission_by_email(self, timestamp: str, email: str) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE created_ts=? AND email=?;
        """
        return self._fetch_one(sql, [timestamp, email])

    def get_commission_by_id(self, commission_id: int) -> Optional[dict]:
        sql = """
            SELECT * FROM commissions WHERE id=?;
        """
        return self._fetch_one(sql, [commission_id])

    def update_ts(self, commission_id: int) -> dict:
        sql = "UPDATE commissions SET updated_ts=CURRENT_TIMESTAMP WHERE id=? RETURNING *;"
        return self._fetch_one(sql, [commission_id])

    def set_preferred_artist(self, commission_id: int, preferred_artist: str, is_exclusive: bool):
        sql = "UPDATE commissions SET preferred_artist=?, is_exclusive=? WHERE id=?;"
        self.cur.execute(sql, [preferred_artist, is_exclusive, commission_id])

    def set_is_exclusive(self, commission_id: int, is_exclusive: bool):
        sql = "UPDATE commissions SET is_exclusive=? WHERE id=?;"
        self.cur.execute(sql, [is_exclusive, commission_id])

    def assign_commission(self, commission_id: int, assigned_to: int):
        sql = "UPDATE commissions SET assigned_to=? WHERE id=?;"
        self.cur.execute(sql, [assigned_to, commission_id])

    def accept_commission(self, commission_id: int, accepted=True):
        sql = "UPDATE commissions SET accepted=? WHERE id=?;"
        self.cur.execute(sql, [accepted, commission_id])

    def invoice_commission(self, commission_id: int, invoiced=True):
        sql = "UPDATE commissions SET invoiced=? WHERE id=?;"
        self.cur.execute(sql, [invoiced, commission_id])

    def pay_commission(self, commission_id: int, paid=True):
        sql = "UPDATE commissions SET paid=? WHERE id=?;"
        self.cur.execute(sql, [paid, commission_id])

    def finish_commission(self, commission_id: int, finished=True):
        sql = "UPDATE commissions SET finished=? WHERE id=?;"
        self.cur.execute(sql, [finished, commission_id])
