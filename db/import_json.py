"""Перенос данных проекта из JSON-файлов в базу SQLite.

Запуск из корня проекта:  python -m db.import_json
Скрипт создаёт таблицы (если их нет) и заново заполняет их данными JSON.
"""

import json
import sqlite3
from pathlib import Path

from db.database import BASE_DIR, get_connection, create_schema

DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> list:
    """Прочитать список записей из JSON-файла каталога data/."""
    with open(DATA_DIR / filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn: sqlite3.Connection) -> None:
    """Очистить таблицы: сначала зависимые, потом основные."""
    for table in ("registrations", "events", "users", "venues"):
        conn.execute(f"DELETE FROM {table}")


def import_venues(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO venues (id, name, address, capacity) "
        "VALUES (?, ?, ?, ?)",
        [
            (venue["id"], venue["name"], venue["address"], venue["capacity"])
            for venue in load_json("venues.json")
        ],
    )


def import_users(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
        [
            (user["id"], user["name"], user["email"])
            for user in load_json("users.json")
        ],
    )


def import_events(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO events (id, title, venue_id, event_date, price, "
        "organizer_id, is_cancelled) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (
                event["id"],
                event["title"],
                event["venue_id"],
                event["event_date"],
                event["price"],
                event["organizer_id"],
                int(event["is_cancelled"]),
            )
            for event in load_json("events.json")
        ],
    )


def import_registrations(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO registrations (id, event_id, user_id) VALUES (?, ?, ?)",
        [
            (reg["id"], reg["event_id"], reg["user_id"])
            for reg in load_json("registrations.json")
        ],
    )


def import_all(db_path: Path = None) -> None:
    """Создать схему и перенести все данные одной транзакцией."""
    conn = get_connection(db_path) if db_path else get_connection()
    try:
        create_schema(conn)
        clear_tables(conn)
        import_venues(conn)
        import_users(conn)
        import_events(conn)
        import_registrations(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    import_all()
    print("Данные перенесены из JSON в SQLite")
