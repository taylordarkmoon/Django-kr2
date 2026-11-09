from django.shortcuts import render

from db.database import fetch_all

UPCOMING_EVENTS_SQL = """
    SELECT id, title, event_date
    FROM events
    WHERE is_cancelled = 0
    ORDER BY event_date
    LIMIT 3;
"""


def index(request):
    context = {
        "upcoming_events": fetch_all(UPCOMING_EVENTS_SQL),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    return render(request, "homepage/page_not_found.html", status=404)
