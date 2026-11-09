from django.shortcuts import render

from db.database import fetch_all, fetch_one

ACTIVE_EVENTS_SQL = """
    SELECT events.id, events.title, events.event_date, events.price,
           venues.name AS venue_name,
           users.name AS organizer_name,
           COUNT(registrations.id) AS participants_count
    FROM events
    JOIN venues ON events.venue_id = venues.id
    JOIN users ON events.organizer_id = users.id
    LEFT JOIN registrations ON registrations.event_id = events.id
    WHERE events.is_cancelled = 0
    GROUP BY events.id
    ORDER BY events.event_date;
"""

CHEAP_EVENTS_SQL = """
    SELECT events.id, events.title, events.event_date, events.price,
           venues.name AS venue_name,
           users.name AS organizer_name,
           COUNT(registrations.id) AS participants_count
    FROM events
    JOIN venues ON events.venue_id = venues.id
    JOIN users ON events.organizer_id = users.id
    LEFT JOIN registrations ON registrations.event_id = events.id
    WHERE events.is_cancelled = 0
      AND events.price <= ?
    GROUP BY events.id
    ORDER BY events.price;
"""

EVENT_SQL = """
    SELECT events.id, events.title, events.event_date, events.price,
           events.is_cancelled,
           venues.id AS venue_id, venues.name AS venue_name,
           venues.capacity AS venue_capacity,
           users.name AS organizer_name, users.email AS organizer_email
    FROM events
    JOIN venues ON events.venue_id = venues.id
    JOIN users ON events.organizer_id = users.id
    WHERE events.id = ?;
"""

PARTICIPANTS_SQL = """
    SELECT users.name, users.email
    FROM registrations
    JOIN users ON registrations.user_id = users.id
    WHERE registrations.event_id = ?
    ORDER BY users.name;
"""

EVENTS_COUNT_SQL = """
    SELECT COUNT(*) AS events_count
    FROM events
    WHERE is_cancelled = 0;
"""

PRICES_SQL = """
    SELECT MIN(price) AS min_price,
           ROUND(AVG(price)) AS avg_price,
           MAX(price) AS max_price
    FROM events
    WHERE is_cancelled = 0;
"""

EVENTS_BY_VENUE_SQL = """
    SELECT venues.name AS venue_name,
           COUNT(events.id) AS events_count
    FROM venues
    LEFT JOIN events
        ON venues.id = events.venue_id
       AND events.is_cancelled = 0
    GROUP BY venues.id, venues.name
    ORDER BY events_count DESC, venues.name;
"""

OCCUPANCY_SQL = """
    SELECT events.title,
           venues.capacity,
           COUNT(registrations.id) AS participants_count,
           venues.capacity - COUNT(registrations.id) AS free_seats
    FROM events
    JOIN venues ON events.venue_id = venues.id
    LEFT JOIN registrations ON registrations.event_id = events.id
    WHERE events.is_cancelled = 0
    GROUP BY events.id
    ORDER BY participants_count DESC;
"""

EVENTS_BY_ORGANIZER_SQL = """
    SELECT users.name AS organizer_name,
           COUNT(events.id) AS events_count,
           SUM(events.is_cancelled) AS cancelled_count
    FROM users
    JOIN events ON events.organizer_id = users.id
    GROUP BY users.id, users.name
    ORDER BY events_count DESC;
"""

POPULAR_VENUES_SQL = """
    SELECT venues.name AS venue_name,
           COUNT(events.id) AS events_count
    FROM venues
    JOIN events ON venues.id = events.venue_id
    WHERE events.is_cancelled = 0
    GROUP BY venues.id, venues.name
    HAVING COUNT(events.id) > ?
    ORDER BY events_count DESC;
"""


def events(request):
    max_price = request.GET.get("max_price", "")
    if max_price.isdigit():
        events_list = fetch_all(CHEAP_EVENTS_SQL, (int(max_price),))
    else:
        max_price = ""
        events_list = fetch_all(ACTIVE_EVENTS_SQL)
    context = {
        "events": events_list,
        "max_price": max_price,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    event = fetch_one(EVENT_SQL, (event_id,))
    context = {"event": event}
    if event is not None:
        context["participants"] = fetch_all(PARTICIPANTS_SQL, (event_id,))
    return render(
        request,
        "events/event_detail.html",
        context,
        status=404 if event is None else 200,
    )


def statistics(request):
    context = {
        "events_count": fetch_one(EVENTS_COUNT_SQL)["events_count"],
        "prices": fetch_one(PRICES_SQL),
        "by_venue": fetch_all(EVENTS_BY_VENUE_SQL),
        "occupancy": fetch_all(OCCUPANCY_SQL),
        "by_organizer": fetch_all(EVENTS_BY_ORGANIZER_SQL),
        "popular_venues": fetch_all(POPULAR_VENUES_SQL, (1,)),
    }
    return render(request, "events/statistics.html", context)
