import pytest

from models import Venue
from models.venues import (
    add_venue,
    check_venue_capacity,
    filter_venues_by_capacity,
    find_venue,
    find_venue_by_id,
    sort_venues,
)


def test_venue_creation():
    venue = Venue(1, "Лофт", "Лесная ул., 5", 60)
    assert venue.id == 1
    assert venue.name == "Лофт"
    assert venue.capacity == 60
    assert "Лофт" in str(venue)


def test_venue_is_suitable_for():
    venue = Venue(1, "Лофт", "Лесная ул., 5", 60)
    assert venue.is_suitable_for(60)
    assert not venue.is_suitable_for(61)


def test_add_venue_and_find():
    venues = []
    add_venue(venues, "Конференц-зал", "ул. Тверская, 12", 120)
    add_venue(venues, "Коворкинг", "пр. Вернадского, 78", 25)
    assert len(venues) == 2
    assert venues[1].id == 2
    assert find_venue(venues, "зал") == [venues[0]]
    assert find_venue_by_id(venues, 2) is venues[1]
    assert find_venue_by_id(venues, 99) is None


def test_add_venue_wrong_capacity():
    with pytest.raises(ValueError):
        add_venue([], "Зал", "Адрес", 0)


def test_capacity_filter_and_sort():
    venues = [
        Venue(1, "A", "a", 120),
        Venue(2, "B", "b", 25),
        Venue(3, "C", "c", 60),
    ]
    assert check_venue_capacity(venues, 3, 50)
    assert not check_venue_capacity(venues, 2, 50)
    assert len(filter_venues_by_capacity(venues, 50)) == 2
    assert [v.capacity for v in sort_venues(venues)] == [25, 60, 120]
