from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.events import is_venue_available
from models.venues import find_venue_by_id, sort_venues
from storage import load_events, load_users, load_venues


def venues(request):
    items = ""
    for venue in sort_venues(load_venues()):
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/venues/{venue.id}/">{venue.name}</a>
            <span class="text-muted">до {venue.capacity} чел.</span>
        </li>
        """
    content = f"""
    <h1>Площадки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Event – площадки", content))


def venue_detail(request, venue_id):
    venues_list = load_venues()
    venue = find_venue_by_id(venues_list, venue_id)
    if venue is None:
        content = """
        <h1 class="text-danger">Площадка не найдена</h1>
        <a href="/venues/" class="btn btn-outline-secondary">
            ← к списку площадок
        </a>
        """
        return HttpResponse(
            page("Площадка не найдена", content),
            status=404,
        )
    events_list = load_events(venues_list, load_users())
    available = is_venue_available(
        events_list,
        venue,
        date.today().isoformat(),
    )
    status = "свободна" if available else "занята"
    badge = "bg-success" if available else "bg-danger"
    items = ""
    for event in events_list:
        if event.venue.id == venue.id and not event.is_cancelled:
            items += f"""
            <li class="list-group-item">
                <a href="/events/{event.id}/">{event.title}</a>
                – {event.event_date}
            </li>
            """
    if not items:
        items = '<li class="list-group-item">Мероприятий нет</li>'
    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{venue.name}</h5>
            <p class="card-text"><strong>Адрес:</strong> {venue.address}</p>
            <p class="card-text">
                <strong>Вместимость:</strong> {venue.capacity} чел.
            </p>
            <p class="card-text">
                Сегодня площадка
                <span class="badge {badge}">{status}</span>
            </p>
        </div>
    </div>
    <h4>Мероприятия на площадке</h4>
    <ul class="list-group mb-3">{items}</ul>
    <a href="/venues/" class="btn btn-outline-secondary">
        ← к списку площадок
    </a>
    """
    return HttpResponse(page(venue.name, content), status=200)
