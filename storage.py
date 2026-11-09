"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json
from pathlib import Path
from typing import List

from models import Event, Registration, User, Venue
from models.events import find_event_by_id
from models.users import find_user_by_id
from models.venues import find_venue_by_id

DATA_DIR = Path(__file__).resolve().parent / "data"
VENUES_FILE = DATA_DIR / "venues.json"
USERS_FILE = DATA_DIR / "users.json"
EVENTS_FILE = DATA_DIR / "events.json"
REGISTRATIONS_FILE = DATA_DIR / "registrations.json"


def read_json(filename: Path) -> list:
    """Прочитать список записей из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, данные будут пустыми")
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные будут пустыми")
    return []


def write_json(filename: Path, records: list) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_venues(filename: Path = VENUES_FILE) -> List[Venue]:
    """Загрузить площадки: JSON → объекты Venue."""
    return [
        Venue(data["id"], data["name"], data["address"], data["capacity"])
        for data in read_json(filename)
    ]


def save_venues(venues: List[Venue], filename: Path = VENUES_FILE) -> None:
    """Сохранить площадки: объекты Venue → JSON."""
    write_json(filename, [
        {
            "id": venue.id,
            "name": venue.name,
            "address": venue.address,
            "capacity": venue.capacity,
        }
        for venue in venues
    ])


def load_users(filename: Path = USERS_FILE) -> List[User]:
    """Загрузить пользователей: JSON → объекты User."""
    return [User.from_data(data) for data in read_json(filename)]


def save_users(users: List[User], filename: Path = USERS_FILE) -> None:
    """Сохранить пользователей: объекты User → JSON."""
    write_json(filename, [
        {"id": user.id, "name": user.name, "email": user.email}
        for user in users
    ])


def load_events(
    venues: List[Venue],
    users: List[User],
    filename: Path = EVENTS_FILE,
) -> List[Event]:
    """Загрузить мероприятия и связать их с площадками и организаторами."""
    events = []
    for data in read_json(filename):
        venue = find_venue_by_id(venues, data["venue_id"])
        organizer = find_user_by_id(users, data["organizer_id"])
        if venue is None or organizer is None:
            print(f"Мероприятие {data['id']} пропущено: нет связанных данных")
            continue
        event = Event(
            data["id"],
            data["title"],
            venue,
            data["event_date"],
            data["price"],
            organizer,
        )
        event.is_cancelled = data["is_cancelled"]
        events.append(event)
    return events


def save_events(events: List[Event], filename: Path = EVENTS_FILE) -> None:
    """Сохранить мероприятия: вместо объектов записываются их id."""
    write_json(filename, [
        {
            "id": event.id,
            "title": event.title,
            "venue_id": event.venue.id,
            "event_date": event.event_date,
            "price": event.price,
            "organizer_id": event.organizer.id,
            "is_cancelled": event.is_cancelled,
        }
        for event in events
    ])


def load_registrations(
    events: List[Event],
    users: List[User],
    filename: Path = REGISTRATIONS_FILE,
) -> List[Registration]:
    """Загрузить регистрации и связать их с мероприятиями и участниками."""
    registrations = []
    for data in read_json(filename):
        event = find_event_by_id(events, data["event_id"])
        user = find_user_by_id(users, data["user_id"])
        if event is None or user is None:
            continue
        registrations.append(Registration(data["id"], event, user))
    return registrations


def save_registrations(
    registrations: List[Registration],
    filename: Path = REGISTRATIONS_FILE,
) -> None:
    """Сохранить регистрации: вместо объектов записываются их id."""
    write_json(filename, [
        {"id": reg.id, "event_id": reg.event.id, "user_id": reg.user.id}
        for reg in registrations
    ])


def load_all() -> tuple:
    """Загрузить все данные проекта с восстановлением связей."""
    venues = load_venues()
    users = load_users()
    events = load_events(venues, users)
    registrations = load_registrations(events, users)
    return venues, users, events, registrations
