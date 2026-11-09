from models import Event, User, Venue
from models.registrations import count_participants, register_participant


def make_event(capacity):
    venue = Venue(1, "Коворкинг", "пр. Вернадского, 78", capacity)
    organizer = User(1, "Анна Смирнова", "anna@example.com")
    return Event(1, "Митап", venue, "2026-11-20", 300, organizer)


def test_register_participant():
    event = make_event(10)
    user = User(2, "Иван Петров", "ivan@example.com")
    registrations = []
    assert register_participant(registrations, event, user)
    assert count_participants(registrations, event) == 1


def test_no_double_registration():
    event = make_event(10)
    user = User(2, "Иван Петров", "ivan@example.com")
    registrations = []
    register_participant(registrations, event, user)
    assert register_participant(registrations, event, user) is None


def test_no_seats_left():
    event = make_event(1)
    registrations = []
    register_participant(registrations, event, User(2, "Иван", "i@e.ru"))
    second_user = User(3, "Мария", "m@e.ru")
    assert register_participant(registrations, event, second_user) is None


def test_cancelled_event_registration():
    event = make_event(10)
    event.cancel()
    user = User(2, "Иван Петров", "ivan@example.com")
    assert register_participant([], event, user) is None
