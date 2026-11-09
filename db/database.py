"""Подключение к базе данных SQLite проекта Event."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "event.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Открыть соединение с базой.

    Включается проверка внешних ключей, а строки результата
    возвращаются как sqlite3.Row – к полям можно обращаться по имени.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Создать таблицы по файлу sql/schema.sql."""
    with open(SCHEMA_PATH, encoding="utf-8") as file:
        conn.executescript(file.read())


def fetch_all(query: str, params: tuple = ()) -> list:
    """Выполнить запрос и вернуть все строки результата."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def fetch_one(query: str, params: tuple = ()):
    """Выполнить запрос и вернуть одну строку или None."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()
