# Event – сервис мероприятий

## Назначение

Event – приложение для организации мероприятий. Организаторы создают
мероприятия и выбирают для них площадки, участники записываются на
мероприятия и видят стоимость билета.

Консольная версия приложения (ПР1–ПР3) дополнена веб-интерфейсом на Django (ПР5),
который в ПР6 переведён на систему шаблонов Django, а в ПР7 получает данные
из базы SQLite с помощью SQL-запросов.

Приложение позволяет:

* просматривать площадки и мероприятия в браузере;
* просматривать информацию о конкретной площадке и мероприятии;
* проверять, свободна ли площадка на дату;
* видеть стоимость билета и список участников мероприятия;
* создавать и отменять мероприятия (консольная версия);
* записываться на мероприятия с учётом вместимости площадки (консольная версия);
* хранить данные между запусками приложения.

## Используемые технологии

* Python 3;
* Django 5.2 – веб-фреймворк;
* Django Template Language (DTL) – шаблоны страниц;
* HTML – разметка веб-страниц;
* CSS (собственный `style.css`) и Bootstrap 5.3 – оформление страниц;
* JavaScript (`main.js`) – текущий год в подвале, подсветка пункта меню;
* SQLite и SQL (модуль `sqlite3`) – хранение и выборка данных;
* JSON – исходные данные, перенесённые в базу;
* pytest – автоматизированные тесты;
* flake8 – проверка качества кода.

## Целевая аудитория

Организаторы небольших мероприятий (митапов, мастер-классов, концертов)
и люди, которые ищут, куда сходить, и хотят записаться на мероприятие.

## Предметная область

Основные объекты: площадка, пользователь, мероприятие, регистрация участника.

* Организатор создаёт мероприятие на площадке на определённую дату.
* На одной площадке в один день может быть только одно активное мероприятие.
* Отменённое мероприятие не занимает площадку.
* Участник может записаться на мероприятие один раз; число участников
  не может превышать вместимость площадки.

## Основные сущности

### Venue – площадка

Атрибуты: `id`, `name`, `address`, `capacity`.
Методы: `is_suitable_for()` – хватит ли мест, `validate_capacity()`
(`@staticmethod`), `__str__()`.

### User – пользователь

Атрибуты: `id`, `name`, `email`.
Методы: `from_data()` (`@classmethod`), `__str__()`.

### Event – мероприятие

Атрибуты: `id`, `title`, `venue` (объект `Venue`), `event_date`, `price`,
`organizer` (объект `User`), `is_cancelled`.
Методы: `cancel()`, `get_price_text()`, `__str__()`.

### Registration – регистрация участника

Атрибуты: `id`, `event` (объект `Event`), `user` (объект `User`).
Методы: `__str__()`.

## Страницы веб-интерфейса

| URL | Имя маршрута | Что показывает | SQL |
|-----|--------------|----------------|-----|
| `/` | `homepage:index` | ближайшие мероприятия | `ORDER BY` + `LIMIT` |
| `/venues/` | `venues:list` | площадки, фильтр `?min_capacity=` | `SELECT`, `WHERE` |
| `/venues/available/` | `venues:available` | свободные площадки на дату `?date=` | подзапрос `NOT IN` |
| `/venues/<int:venue_id>/` | `venues:detail` | площадка и её мероприятия | `WHERE id = ?` |
| `/events/` | `events:list` | активные мероприятия, фильтр `?max_price=` | `JOIN`, `COUNT`, `GROUP BY` |
| `/events/<int:event_id>/` | `events:detail` | мероприятие, площадка, организатор, участники | `JOIN` |
| `/events/statistics/` | `events:statistics` | статистика | `COUNT`, `MIN/AVG/MAX`, `GROUP BY`, `HAVING` |

Если площадка или мероприятие не найдены, сообщение выводится в шаблоне
через `{% if %} / {% else %}`, а `render()` возвращает ответ со статусом 404.
Для адресов без маршрута работает `handler404` →
`homepage.views.page_not_found()` → шаблон `homepage/page_not_found.html`.

## База данных SQLite (ПР7)

Файл базы: `data/event.sqlite`. Таблицы создаются командами из
`sql/schema.sql`, данные переносятся из JSON скриптом `db/import_json.py`.

| Таблица | Поля (тип) | Ключи |
|---------|-----------|-------|
| `venues` | `id` INTEGER, `name` TEXT, `address` TEXT, `capacity` INTEGER | PK `id` |
| `users` | `id` INTEGER, `name` TEXT, `email` TEXT (UNIQUE) | PK `id` |
| `events` | `id` INTEGER, `title` TEXT, `venue_id` INTEGER, `event_date` TEXT (ГГГГ-ММ-ДД), `price` INTEGER, `organizer_id` INTEGER, `is_cancelled` INTEGER (0/1) | PK `id`; FK `venue_id → venues.id`, `organizer_id → users.id` |
| `registrations` | `id` INTEGER, `event_id` INTEGER, `user_id` INTEGER | PK `id`; FK `event_id → events.id`, `user_id → users.id`; UNIQUE (`event_id`, `user_id`) |

Связи: на площадке проходит много мероприятий; организатор создаёт много
мероприятий; на мероприятие записывается много участников.

* `db/database.py` – `get_connection()` (включает `PRAGMA foreign_keys = ON`
  и `row_factory = sqlite3.Row`), `create_schema()`, помощники `fetch_all()`
  и `fetch_one()` для представлений;
* `db/import_json.py` – создание таблиц и перенос данных из JSON
  одной транзакцией (`commit` / `rollback`);
* `sql/queries.sql` – 14 проверенных запросов: списки (`ORDER BY`, `LIMIT`),
  фильтрация (`WHERE`, подзапрос `NOT IN`), соединения (`JOIN`,
  `LEFT JOIN`), агрегатные функции (`COUNT`, `MIN`, `AVG`, `MAX`, `SUM`),
  группировка (`GROUP BY`) и фильтрация групп (`HAVING`).

Значения от пользователя (дата, вместимость, цена, id) передаются в запросы
только параметрами `?`. Django ORM пока не используется – запросы
выполняются модулем `sqlite3`.

Создание и заполнение базы (из корня проекта):

```text
python -m db.import_json
```

## Шаблоны Django (ПР6)

HTML больше не формируется в Python: view-функции получают данные
(с ПР7 – из SQLite), собирают словарь `context` и вызывают
`render(request, "шаблон.html", context)`. Функция `page()` из ПР5 удалена.

* **Базовый шаблон** `templates/base.html` – HTML-каркас, Bootstrap,
  собственный CSS, логотип, навигация, подвал, JavaScript; блоки
  `{% block title %}` и `{% block content %}`.
* **Наследование** – все страницы начинаются с `{% extends "base.html" %}`.
* **Включаемые шаблоны** (`{% include %}`):
  `templates/includes/navigation.html` – меню сайта;
  `venues/includes/venue_card.html` – карточка площадки;
  `events/includes/event_status.html` – статус мероприятия
  (используется и в списке, и на странице мероприятия).
* **Циклы и условия** – `{% for ... %}{% empty %}` для списков,
  `{% if event.is_cancelled %}`, `{% if is_free_today %}`, `{% if venue %}`.
* **Именованные URL и пространства имён** – `app_name` в `urls.py`
  приложений, ссылки вида `{% url 'events:detail' event.id %}`.
* **Фильтры** – `{{ venues|length }}`, `{{ participants|length }}`,
  `{{ venue.name|default:"Без названия" }}`. Дата мероприятия хранится
  строкой и выводится без преобразования.
* **Статические файлы** – `{% load static %}`, каталог
  `homepage/static/homepage/`: `css/style.css`, `js/main.js`, `img/logo.png`.

## Основные операции

### Используется в веб-интерфейсе (ПР5)

* просмотр площадок и мероприятий;
* просмотр карточки площадки и мероприятия;
* проверка, свободна ли площадка на текущую дату (`is_venue_available()`);
* вывод стоимости билета (`Event.get_price_text()`) и участников (`get_participants()`);
* список мероприятий площадки (`get_venue_events()`, добавлена в ПР6).

### Отложено до следующих работ

Реализовано в ПР3 и работает в консольной версии; в вебе появится вместе
с формами и POST-запросами:

* добавление площадки, поиск и сортировка площадок;
* создание и отмена мероприятия;
* запись участника на мероприятие.

## Хранение данных

Данные хранятся в JSON-файлах каталога `data/`:
`venues.json`, `users.json`, `events.json`, `registrations.json`.

При загрузке данные JSON превращаются в объекты `Venue`, `User`, `Event`,
`Registration`; связи восстанавливаются по `venue_id`, `organizer_id`,
`event_id`, `user_id`. JSON-хранилище использует консольная версия
(`main.py`), а веб-версия с ПР7 читает данные из `data/event.sqlite`,
куда они перенесены скриптом `db/import_json.py`. Формы ещё не реализованы.

## Структура проекта

```text
event_service/
├── README.md
├── requirements.txt
├── setup.cfg            # настройки flake8 и pytest
├── manage.py
├── main.py              # консольная версия (ПР3)
├── storage.py
├── utils.py
├── db/                  # работа с SQLite (ПР7)
│   ├── database.py
│   └── import_json.py
├── sql/
│   ├── schema.sql       # создание таблиц
│   └── queries.sql      # SQL-запросы проекта
├── templates/           # шаблоны уровня проекта
│   ├── base.html
│   └── includes/
│       └── navigation.html
├── event_site/          # пакет настроек Django-проекта
│   ├── settings.py
│   └── urls.py
├── homepage/
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── page_not_found.html
│   ├── urls.py
│   └── views.py
├── venues/
│   ├── templates/venues/
│   │   ├── venue_list.html
│   │   ├── venue_detail.html
│   │   └── includes/venue_card.html
│   ├── urls.py
│   └── views.py
├── events/
│   ├── templates/events/
│   │   ├── event_list.html
│   │   ├── event_detail.html
│   │   └── includes/event_status.html
│   ├── urls.py
│   └── views.py
├── models/              # классы предметной области (ПР3)
├── data/                # JSON-файлы и база event.sqlite
└── tests/
```

## Запуск приложения

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python -m db.import_json
python manage.py runserver
```

Открыть в браузере `http://127.0.0.1:8000/`.

Консольная версия (сохранена): `python main.py`.

## Тестирование и качество кода

```text
python manage.py check
pytest -v
flake8 . --extend-exclude=venv
```

## Текущее состояние и план развития

Реализовано:

* ПР5 – Django-проект `event_site`, приложения `homepage`, `venues`,
  `events`, маршрутизация, view-функции, страница 404;
* ПР6 – шаблоны Django: `base.html`, наследование, блоки, `include`,
  контекст, циклы и условия, именованные URL с пространствами имён,
  фильтры, собственные CSS, JavaScript и логотип;
* ПР7 – база SQLite `data/event.sqlite`: схема `sql/schema.sql`, перенос
  данных из JSON, 14 SQL-запросов в `sql/queries.sql`; страницы получают
  данные SQL-запросами; добавлены поиск свободных площадок на дату,
  фильтры по вместимости и цене, страница статистики.

Django ORM и формы пока не используются.

Планируется:

* подключение базы к Django через Django ORM (модели и миграции), PostgreSQL;
* формы создания мероприятий и записи участников;
* регистрация, вход и личный кабинет пользователя;
* REST API, Docker, CI/CD.
