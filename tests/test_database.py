import sqlite3

import pytest

from db.database import get_connection
from db.import_json import import_all


@pytest.fixture
def conn(tmp_path):
    db_path = tmp_path / "test.sqlite"
    import_all(db_path)
    connection = get_connection(db_path)
    yield connection
    connection.close()


def test_tables_created(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
    ).fetchall()
    names = [row["name"] for row in rows]
    assert names == ["events", "registrations", "users", "venues"]


def test_data_imported(conn):
    count = conn.execute("SELECT COUNT(*) FROM venues").fetchone()[0]
    assert count == 3
    event = conn.execute("SELECT * FROM events WHERE id = 3").fetchone()
    assert event["is_cancelled"] == 1


def test_foreign_key_is_checked(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO events (title, venue_id, event_date, organizer_id) "
            "VALUES ('Тест', 999, '2026-12-01', 1)"
        )


def test_free_venues_on_date(conn):
    rows = conn.execute(
        """
        SELECT id FROM venues
        WHERE id NOT IN (
            SELECT venue_id FROM events
            WHERE event_date = ? AND is_cancelled = 0
        )
        """,
        ("2026-11-20",),
    ).fetchall()
    assert sorted(row["id"] for row in rows) == [2, 3]
