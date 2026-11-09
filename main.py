"""Консольная версия сервиса мероприятий Event (ПР1–ПР3)."""

from typing import List

from models import Event, Registration, User, Venue
from models.events import (
    cancel_event,
    create_event,
    find_event_by_id,
    get_event_status,
    is_venue_available,
    show_events,
)
from models.registrations import (
    count_participants,
    register_participant,
)
from models.users import find_user_by_id, show_users
from models.venues import (
    add_venue,
    find_venue,
    find_venue_by_id,
    show_venues,
    sort_venues,
)
from storage import (
    load_all,
    save_events,
    save_registrations,
    save_users,
    save_venues,
)
from utils import input_date, input_int

MENU = """
=== Event – сервис мероприятий ===
1. Показать площадки
2. Найти площадку по названию
3. Добавить площадку
4. Проверить, свободна ли площадка на дату
5. Показать мероприятия
6. Создать мероприятие
7. Отменить мероприятие
8. Записаться на мероприятие
9. Показать пользователей
0. Выход"""


def create_new_event(
    events: List[Event],
    venues: List[Venue],
    users: List[User],
) -> None:
    """Сценарий создания мероприятия организатором."""
    venue = find_venue_by_id(venues, input_int("ID площадки: "))
    organizer = find_user_by_id(users, input_int("ID организатора: "))
    if venue is None or organizer is None:
        print("Площадка или организатор не найдены")
        return
    title = input("Название мероприятия: ")
    event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    price = input_int("Цена билета, руб. (0 – бесплатно): ")
    event = create_event(events, title, venue, event_date, price, organizer)
    if event is None:
        print(get_event_status(False))
    else:
        print(f"Мероприятие создано, номер {event.id}")


def register_new_participant(
    registrations: List[Registration],
    events: List[Event],
    users: List[User],
) -> None:
    """Сценарий записи участника на мероприятие."""
    event = find_event_by_id(events, input_int("ID мероприятия: "))
    user = find_user_by_id(users, input_int("ID участника: "))
    if event is None or user is None:
        print("Мероприятие или участник не найдены")
        return
    if register_participant(registrations, event, user) is None:
        print("Записаться нельзя: мест нет, запись уже есть "
              "или мероприятие отменено")
        return
    taken = count_participants(registrations, event)
    print(f"Вы записаны. Стоимость билета: {event.get_price_text()}")
    print(f"Занято мест: {taken} из {event.venue.capacity}")


def main() -> None:
    """Точка запуска консольного приложения."""
    venues, users, events, registrations = load_all()
    while True:
        print(MENU)
        choice = input("Выберите действие: ")
        if choice == "1":
            show_venues(sort_venues(venues))
        elif choice == "2":
            show_venues(find_venue(venues, input("Название: ")))
        elif choice == "3":
            try:
                add_venue(
                    venues,
                    input("Название: "),
                    input("Адрес: "),
                    input_int("Вместимость: "),
                )
            except ValueError as error:
                print(error)
        elif choice == "4":
            venue = find_venue_by_id(venues, input_int("ID площадки: "))
            if venue is None:
                print("Площадка не найдена")
                continue
            event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
            print(get_event_status(
                is_venue_available(events, venue, event_date)
            ))
        elif choice == "5":
            show_events(events)
        elif choice == "6":
            create_new_event(events, venues, users)
        elif choice == "7":
            if not cancel_event(events, input_int("ID мероприятия: ")):
                print("Мероприятие не найдено или уже отменено")
        elif choice == "8":
            register_new_participant(registrations, events, users)
        elif choice == "9":
            show_users(users)
        elif choice == "0":
            break
        else:
            print("Нет такого пункта меню")
    save_venues(venues)
    save_users(users)
    save_events(events)
    save_registrations(registrations)
    print("Данные сохранены")


if __name__ == "__main__":
    main()
