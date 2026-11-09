"""Мероприятия и функции работы с ними."""

from typing import List, Optional

from .users import User
from .venues import Venue


class Event:
    """Мероприятие, которое организатор проводит на площадке."""

    def __init__(
        self,
        event_id: int,
        title: str,
        venue: Venue,
        event_date: str,
        price: int,
        organizer: User,
    ) -> None:
        """Создать объект мероприятия."""
        self.id = event_id
        self.title = title
        self.venue = venue
        self.event_date = event_date
        self.price = price
        self.organizer = organizer
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменить мероприятие."""
        self.is_cancelled = True

    def get_price_text(self) -> str:
        """Вернуть стоимость билета в виде текста."""
        if self.price == 0:
            return "бесплатно"
        return f"{self.price} руб."

    def __str__(self) -> str:
        """Вернуть строковое представление мероприятия."""
        status = "отменено" if self.is_cancelled else "активно"
        return (
            f"[{self.id}] {self.title} – {self.event_date}, "
            f"{self.venue.name}, билет: {self.get_price_text()} ({status})"
        )


def is_venue_available(
    events: List[Event],
    venue: Venue,
    event_date: str,
) -> bool:
    """Проверить, свободна ли площадка на дату.

    Отменённые мероприятия площадку не занимают.
    """
    for event in events:
        if (
            event.venue.id == venue.id
            and event.event_date == event_date
            and not event.is_cancelled
        ):
            return False
    return True


def get_venue_events(events: List[Event], venue: Venue) -> List[Event]:
    """Вернуть активные мероприятия, проходящие на площадке."""
    return [
        event for event in events
        if event.venue.id == venue.id and not event.is_cancelled
    ]


def create_event(
    events: List[Event],
    title: str,
    venue: Venue,
    event_date: str,
    price: int,
    organizer: User,
) -> Optional[Event]:
    """Создать мероприятие, если площадка свободна на эту дату."""
    if not is_venue_available(events, venue, event_date):
        return None
    new_id = max((event.id for event in events), default=0) + 1
    event = Event(new_id, title, venue, event_date, price, organizer)
    events.append(event)
    return event


def find_event_by_id(
    events: List[Event],
    event_id: int,
) -> Optional[Event]:
    """Найти мероприятие по идентификатору."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def cancel_event(events: List[Event], event_id: int) -> bool:
    """Отменить мероприятие по идентификатору."""
    event = find_event_by_id(events, event_id)
    if event is None or event.is_cancelled:
        return False
    event.cancel()
    return True


def get_event_status(is_available: bool) -> str:
    """Вернуть текстовый статус площадки (функция из ПР1)."""
    if is_available:
        return "Площадка свободна для проведения мероприятия"
    return "Площадка уже занята"


def show_events(events: List[Event]) -> None:
    """Вывести список мероприятий в консоль."""
    if not events:
        print("Мероприятий нет")
        return
    for event in events:
        print(event)
