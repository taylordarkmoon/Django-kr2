"""Площадки для проведения мероприятий."""

from typing import List, Optional


class Venue:
    """Площадка, на которой проводятся мероприятия."""

    def __init__(
        self,
        venue_id: int,
        name: str,
        address: str,
        capacity: int,
    ) -> None:
        """Создать объект площадки."""
        self.id = venue_id
        self.name = name
        self.address = address
        self.capacity = capacity

    def is_suitable_for(self, people_count: int) -> bool:
        """Проверить, поместится ли на площадке people_count человек."""
        return self.capacity >= people_count

    @staticmethod
    def validate_capacity(capacity: int) -> bool:
        """Проверить корректность вместимости."""
        return capacity > 0

    def __str__(self) -> str:
        """Вернуть строковое представление площадки."""
        return (
            f"[{self.id}] {self.name}, {self.address} "
            f"(до {self.capacity} чел.)"
        )


def add_venue(
    venues: List[Venue],
    name: str,
    address: str,
    capacity: int,
) -> Venue:
    """Создать площадку и добавить её в коллекцию."""
    if not Venue.validate_capacity(capacity):
        raise ValueError("Вместимость должна быть больше нуля")
    new_id = max((venue.id for venue in venues), default=0) + 1
    venue = Venue(new_id, name, address, capacity)
    venues.append(venue)
    return venue


def find_venue(venues: List[Venue], query: str) -> List[Venue]:
    """Найти площадки по подстроке названия."""
    query = query.lower()
    return [venue for venue in venues if query in venue.name.lower()]


def find_venue_by_id(
    venues: List[Venue],
    venue_id: int,
) -> Optional[Venue]:
    """Найти площадку по идентификатору."""
    for venue in venues:
        if venue.id == venue_id:
            return venue
    return None


def check_venue_capacity(
    venues: List[Venue],
    venue_id: int,
    people_count: int,
) -> bool:
    """Найти площадку и проверить, хватит ли мест."""
    venue = find_venue_by_id(venues, venue_id)
    if venue is None:
        return False
    return venue.is_suitable_for(people_count)


def filter_venues_by_capacity(
    venues: List[Venue],
    min_capacity: int,
) -> List[Venue]:
    """Отобрать площадки вместимостью не меньше min_capacity."""
    return list(
        venue for venue in venues if venue.is_suitable_for(min_capacity)
    )


def sort_venues(venues: List[Venue]) -> List[Venue]:
    """Отсортировать площадки по вместимости."""
    return sorted(venues, key=lambda venue: venue.capacity)


def show_venues(venues: List[Venue]) -> None:
    """Вывести список площадок в консоль."""
    if not venues:
        print("Площадок нет")
        return
    for venue in venues:
        print(venue)
