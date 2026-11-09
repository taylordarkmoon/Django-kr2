from datetime import date

from django.shortcuts import render

from db.database import fetch_all, fetch_one

VENUES_SQL = """
    SELECT id, name, address, capacity
    FROM venues
    ORDER BY name;
"""

VENUES_BY_CAPACITY_SQL = """
    SELECT id, name, address, capacity
    FROM venues
    WHERE capacity >= ?
    ORDER BY capacity;
"""

VENUE_SQL = """
    SELECT id, name, address, capacity
    FROM venues
    WHERE id = ?;
"""

VENUE_EVENTS_SQL = """
    SELECT id, title, event_date
    FROM events
    WHERE venue_id = ? AND is_cancelled = 0
    ORDER BY event_date;
"""

FREE_VENUES_SQL = """
    SELECT venues.id, venues.name, venues.address, venues.capacity
    FROM venues
    WHERE venues.id NOT IN (
        SELECT events.venue_id
        FROM events
        WHERE events.event_date = ?
          AND events.is_cancelled = 0
    )
    ORDER BY venues.name;
"""


def venues(request):
    min_capacity = request.GET.get("min_capacity", "")
    if min_capacity.isdigit():
        venues_list = fetch_all(VENUES_BY_CAPACITY_SQL, (int(min_capacity),))
    else:
        min_capacity = ""
        venues_list = fetch_all(VENUES_SQL)
    context = {
        "venues": venues_list,
        "min_capacity": min_capacity,
    }
    return render(request, "venues/venue_list.html", context)


def venue_detail(request, venue_id):
    venue = fetch_one(VENUE_SQL, (venue_id,))
    context = {"venue": venue}
    if venue is not None:
        today = date.today().isoformat()
        free_today = fetch_all(FREE_VENUES_SQL, (today,))
        context["is_free_today"] = any(
            row["id"] == venue_id for row in free_today
        )
        context["venue_events"] = fetch_all(VENUE_EVENTS_SQL, (venue_id,))
    return render(
        request,
        "venues/venue_detail.html",
        context,
        status=404 if venue is None else 200,
    )


def available_venues(request):
    event_date = request.GET.get("date", "")
    venues_list = []
    if event_date:
        venues_list = fetch_all(FREE_VENUES_SQL, (event_date,))
    context = {
        "venues": venues_list,
        "event_date": event_date,
    }
    return render(request, "venues/available.html", context)
