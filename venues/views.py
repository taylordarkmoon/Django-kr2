from datetime import date

from django.shortcuts import render

from models.events import get_venue_events, is_venue_available
from models.venues import find_venue_by_id, sort_venues
from storage import load_events, load_users, load_venues


def venues(request):
    context = {
        "venues": sort_venues(load_venues()),
    }
    return render(request, "venues/venue_list.html", context)


def venue_detail(request, venue_id):
    venues_list = load_venues()
    venue = find_venue_by_id(venues_list, venue_id)
    context = {"venue": venue}
    if venue is not None:
        events_list = load_events(venues_list, load_users())
        context["is_free_today"] = is_venue_available(
            events_list,
            venue,
            date.today().isoformat(),
        )
        context["venue_events"] = get_venue_events(events_list, venue)
    return render(
        request,
        "venues/venue_detail.html",
        context,
        status=404 if venue is None else 200,
    )
