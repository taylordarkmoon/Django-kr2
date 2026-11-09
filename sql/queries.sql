-- ==========================================
-- Event: SQL-запросы проекта
-- Значения с ? в веб-приложении передаются параметрами,
-- здесь для проверки в SQLite подставлены примеры.
-- ==========================================


-- ---------- Выборка списков ----------

-- 1. Список площадок по названию (страница «Площадки»)
SELECT id, name, address, capacity
FROM venues
ORDER BY name;

-- 2. Три ближайших активных мероприятия (главная страница)
SELECT id, title, event_date
FROM events
WHERE is_cancelled = 0
ORDER BY event_date
LIMIT 3;


-- ---------- Фильтрация WHERE ----------

-- 3. Площадки вместимостью не меньше заданной (фильтр на странице «Площадки»)
SELECT id, name, address, capacity
FROM venues
WHERE capacity >= 50          -- в Django: capacity >= ?
ORDER BY capacity;

-- 4. Активные мероприятия с билетом не дороже заданной суммы
SELECT id, title, event_date, price
FROM events
WHERE is_cancelled = 0
  AND price <= 1000           -- в Django: price <= ?
ORDER BY price;

-- 5. Свободные площадки на выбранную дату (страница «Свободные площадки»)
SELECT venues.id, venues.name, venues.address, venues.capacity
FROM venues
WHERE venues.id NOT IN (
    SELECT events.venue_id
    FROM events
    WHERE events.event_date = '2026-11-20'   -- в Django: = ?
      AND events.is_cancelled = 0
)
ORDER BY venues.name;


-- ---------- Соединение таблиц JOIN ----------

-- 6. Активные мероприятия с площадкой, организатором и числом участников
--    (страница «Мероприятия»)
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

-- 7. Полная информация о мероприятии (страница мероприятия)
SELECT events.id, events.title, events.event_date, events.price,
       events.is_cancelled,
       venues.id AS venue_id, venues.name AS venue_name,
       venues.capacity AS venue_capacity,
       users.name AS organizer_name, users.email AS organizer_email
FROM events
JOIN venues ON events.venue_id = venues.id
JOIN users ON events.organizer_id = users.id
WHERE events.id = 1;          -- в Django: = ?

-- 8. Участники мероприятия (страница мероприятия)
SELECT users.name, users.email
FROM registrations
JOIN users ON registrations.user_id = users.id
WHERE registrations.event_id = 1   -- в Django: = ?
ORDER BY users.name;


-- ---------- Агрегатные функции ----------

-- 9. Количество активных мероприятий (страница «Статистика»)
SELECT COUNT(*) AS events_count
FROM events
WHERE is_cancelled = 0;

-- 10. Минимальная, средняя и максимальная цена билета активных мероприятий
SELECT MIN(price) AS min_price,
       ROUND(AVG(price)) AS avg_price,
       MAX(price) AS max_price
FROM events
WHERE is_cancelled = 0;


-- ---------- Группировка GROUP BY ----------

-- 11. Количество активных мероприятий на каждой площадке (страница «Статистика»)
SELECT venues.name AS venue_name,
       COUNT(events.id) AS events_count
FROM venues
LEFT JOIN events
    ON venues.id = events.venue_id
   AND events.is_cancelled = 0
GROUP BY venues.id, venues.name
ORDER BY events_count DESC, venues.name;

-- 12. Заполненность мероприятий: участники и свободные места
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

-- 13. Количество мероприятий у каждого организатора
SELECT users.name AS organizer_name,
       COUNT(events.id) AS events_count,
       SUM(events.is_cancelled) AS cancelled_count
FROM users
JOIN events ON events.organizer_id = users.id
GROUP BY users.id, users.name
ORDER BY events_count DESC;


-- ---------- Фильтрация групп HAVING ----------

-- 14. Площадки, на которых больше одного активного мероприятия
SELECT venues.name AS venue_name,
       COUNT(events.id) AS events_count
FROM venues
JOIN events ON venues.id = events.venue_id
WHERE events.is_cancelled = 0
GROUP BY venues.id, venues.name
HAVING COUNT(events.id) > 1      -- в Django: > ?
ORDER BY events_count DESC;
