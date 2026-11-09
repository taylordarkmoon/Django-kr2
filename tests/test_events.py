from models import Event, User, Venue
from models.events import (
    cancel_event,
    create_event,
    find_event_by_id,
    get_event_status,
    is_venue_available,
)


def make_objects():
    venue = Venue(1, "Лофт", "Лесная ул., 5", 60)
    user = User(1, "Анна Смирнова", "anna@example.com")
    return venue, user


def test_event_creation():
    venue, user = make_objects()
    event = Event(1, "Митап", venue, "2026-11-20", 500, user)
    assert event.venue is venue
    assert event.organizer is user
    assert not event.is_cancelled
    assert event.get_price_text() == "500 руб."


def test_free_event_price():
    venue, user = make_objects()
    event = Event(1, "Митап", venue, "2026-11-20", 0, user)
    assert event.get_price_text() == "бесплатно"


def test_venue_busy_on_same_date():
    venue, user = make_objects()
    events = []
    assert create_event(events, "Митап", venue, "2026-11-20", 0, user)
    assert not is_venue_available(events, venue, "2026-11-20")
    assert create_event(events, "Лекция", venue, "2026-11-20", 0, user) is None
    assert is_venue_available(events, venue, "2026-11-21")


def test_cancelled_event_frees_venue():
    venue, user = make_objects()
    events = []
    event = create_event(events, "Митап", venue, "2026-11-20", 0, user)
    assert cancel_event(events, event.id)
    assert event.is_cancelled
    assert is_venue_available(events, venue, "2026-11-20")
    assert not cancel_event(events, event.id)


def test_find_event_by_id():
    venue, user = make_objects()
    events = []
    event = create_event(events, "Митап", venue, "2026-11-20", 0, user)
    assert find_event_by_id(events, event.id) is event
    assert find_event_by_id(events, 999) is None


def test_get_event_status():
    assert get_event_status(True).startswith("Площадка свободна")
    assert get_event_status(False) == "Площадка уже занята"
