from django.http import HttpResponse

from homepage.views import page
from models.events import find_event_by_id
from models.registrations import get_participants
from storage import load_all


def status_badge(event):
    """Вернуть текст и класс бейджа для статуса мероприятия."""
    if event.is_cancelled:
        return "отменено", "bg-secondary"
    return "активно", "bg-success"


def events(request):
    _, _, events_list, _ = load_all()
    items = ""
    for event in events_list:
        status, badge = status_badge(event)
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <span>
                <a href="/events/{event.id}/">{event.title}</a>
                – {event.event_date}, {event.get_price_text()}
            </span>
            <span class="badge {badge} align-self-center">{status}</span>
        </li>
        """
    content = f"""
    <h1>Мероприятия</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Event – мероприятия", content))


def event_detail(request, event_id):
    _, _, events_list, registrations = load_all()
    event = find_event_by_id(events_list, event_id)
    if event is None:
        content = """
        <h1 class="text-danger">Мероприятие не найдено</h1>
        <a href="/events/" class="btn btn-outline-secondary">
            ← к списку мероприятий
        </a>
        """
        return HttpResponse(
            page("Мероприятие не найдено", content),
            status=404,
        )
    status, badge = status_badge(event)
    participants = get_participants(registrations, event)
    names = "".join(
        f'<li class="list-group-item">{user.name}</li>'
        for user in participants
    )
    if not names:
        names = '<li class="list-group-item">Пока никто не записался</li>'
    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{event.title}</h5>
            <p class="card-text"><strong>Дата:</strong> {event.event_date}</p>
            <p class="card-text">
                <strong>Площадка:</strong>
                <a href="/venues/{event.venue.id}/">{event.venue.name}</a>
            </p>
            <p class="card-text">
                <strong>Организатор:</strong> {event.organizer.name}
            </p>
            <p class="card-text">
                <strong>Билет:</strong> {event.get_price_text()}
            </p>
            <p class="card-text">
                <strong>Участники:</strong>
                {len(participants)} из {event.venue.capacity}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
        </div>
    </div>
    <h4>Список участников</h4>
    <ul class="list-group mb-3">{names}</ul>
    <a href="/events/" class="btn btn-outline-secondary">
        ← к списку мероприятий
    </a>
    """
    return HttpResponse(page(event.title, content), status=200)
