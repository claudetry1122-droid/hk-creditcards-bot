import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.getenv("DATABASE_PATH", "cards_bot.db")


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_cards (
                user_id  INTEGER NOT NULL,
                card_id  TEXT    NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, card_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_prefs (
                user_id    INTEGER PRIMARY KEY,
                reward_pref TEXT NOT NULL DEFAULT 'all'
            )
        """)


@contextmanager
def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def add_card(user_id: int, card_id: str) -> bool:
    """Returns True if added, False if the card was already in the wallet."""
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO user_cards (user_id, card_id) VALUES (?, ?)",
                (user_id, card_id),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def remove_card(user_id: int, card_id: str) -> None:
    with _conn() as conn:
        conn.execute(
            "DELETE FROM user_cards WHERE user_id = ? AND card_id = ?",
            (user_id, card_id),
        )


def get_user_cards(user_id: int) -> list[str]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT card_id FROM user_cards WHERE user_id = ? ORDER BY added_at",
            (user_id,),
        ).fetchall()
    return [row["card_id"] for row in rows]


def clear_user_cards(user_id: int) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM user_cards WHERE user_id = ?", (user_id,))


def get_reward_pref(user_id: int) -> str:
    """Returns 'all', 'cashback', or 'miles'."""
    with _conn() as conn:
        row = conn.execute(
            "SELECT reward_pref FROM user_prefs WHERE user_id = ?", (user_id,)
        ).fetchone()
    return row["reward_pref"] if row else "all"


def set_reward_pref(user_id: int, pref: str) -> None:
    with _conn() as conn:
        conn.execute(
            "INSERT INTO user_prefs (user_id, reward_pref) VALUES (?, ?)"
            " ON CONFLICT(user_id) DO UPDATE SET reward_pref = excluded.reward_pref",
            (user_id, pref),
        )
