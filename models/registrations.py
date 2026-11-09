"""Регистрации участников на мероприятия."""

from typing import List, Optional

from .events import Event
from .users import User


class Registration:
    """Запись участника на мероприятие."""

    def __init__(
        self,
        registration_id: int,
        event: Event,
        user: User,
    ) -> None:
        """Создать объект регистрации."""
        self.id = registration_id
        self.event = event
        self.user = user

    def __str__(self) -> str:
        """Вернуть строковое представление регистрации."""
        return f"[{self.id}] {self.user.name} → {self.event.title}"


def get_participants(
    registrations: List[Registration],
    event: Event,
) -> List[User]:
    """Вернуть участников мероприятия."""
    return [reg.user for reg in registrations if reg.event.id == event.id]


def count_participants(
    registrations: List[Registration],
    event: Event,
) -> int:
    """Посчитать количество участников мероприятия."""
    return len(get_participants(registrations, event))


def register_participant(
    registrations: List[Registration],
    event: Event,
    user: User,
) -> Optional[Registration]:
    """Записать пользователя на мероприятие.

    Запись невозможна, если мероприятие отменено, пользователь
    уже записан или на площадке не осталось мест.
    """
    if event.is_cancelled:
        return None
    participants = get_participants(registrations, event)
    if any(participant.id == user.id for participant in participants):
        return None
    if not event.venue.is_suitable_for(len(participants) + 1):
        return None
    new_id = max((reg.id for reg in registrations), default=0) + 1
    registration = Registration(new_id, event, user)
    registrations.append(registration)
    return registration


def show_registrations(registrations: List[Registration]) -> None:
    """Вывести список регистраций в консоль."""
    for registration in registrations:
        print(registration)
