-- ==========================================
-- Event: структура базы данных
-- ==========================================

-- Площадки, на которых проводятся мероприятия
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

-- Пользователи: организаторы и участники
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

-- Мероприятия: проводятся на площадке, создаются организатором
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    venue_id INTEGER NOT NULL,
    event_date TEXT NOT NULL,
    price INTEGER NOT NULL DEFAULT 0,
    organizer_id INTEGER NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (venue_id) REFERENCES venues(id),
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);

-- Регистрации участников на мероприятия
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
