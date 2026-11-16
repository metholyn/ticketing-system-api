# Lab 2 — Документування програмного коду (Doxygen)

Доменна модель системи продажу квитків на події (Ticketing system),
варіант 14 (Event, Ticket), написана на Python.

## Структура

- `app/person.py` — абстрактний клас `Person` і класи-нащадки `User`, `Organizer` (наслідування)
- `app/venue.py` — клас `Venue`
- `app/event.py` — клас `Event` (залежить від `Organizer` і `Venue`)
- `app/ticket.py` — клас `Ticket` і перелік `TicketStatus` (залежить від `Event` і `User`)
- `app/repository.py` — клас `TicketingRepository`, що агрегує всі сутності
- `app/exceptions.py` — доменні винятки
- `demo.py` — демонстраційний запуск моделі

## Генерація документації

Документація згенерована інструментом **Doxygen** (з graphviz для UML-діаграм
класів та графів викликів):

```bash
doxygen Doxyfile
```

Результат — у папці `docs/html/`. Відкрити `docs/html/index.html` у браузері.

## Запуск демо

```bash
python3 demo.py
```
