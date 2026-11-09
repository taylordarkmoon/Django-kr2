from django.shortcuts import render

from models.events import find_event_by_id
from models.registrations import get_participants
from storage import load_all


def events(request):
    _, _, events_list, _ = load_all()
    context = {
        "events": events_list,
    }
    return render(request, "events/event_list.html", context)


def event_detail(request, event_id):
    _, _, events_list, registrations = load_all()
    event = find_event_by_id(events_list, event_id)
    context = {"event": event}
    if event is not None:
        context["participants"] = get_participants(registrations, event)
    return render(
        request,
        "events/event_detail.html",
        context,
        status=404 if event is None else 200,
    )
