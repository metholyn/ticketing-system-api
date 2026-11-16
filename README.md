# Ticketing System API

Навчальний проєкт: REST API для системи продажу квитків на події (варіант 14:
сутності `Event`, `Ticket`). Виконано в рамках практичних завдань з документування
програмного коду та API.

## Структура репозиторію

| Шлях | Опис |
| --- | --- |
| `app/` | Доменна модель (Person → User/Organizer, Venue, Event, Ticket) |
| `api/` | REST API на FastAPI (CRUD для Event, Ticket та допоміжних ресурсів) |
| `openapi.yaml`, `openapi.json` | OpenAPI 3.1 специфікація, згенерована з коду |
| `sdk/python-client/` | Python SDK-клієнт, згенерований `openapi-python-client` |
| `zudoku-docs/` | Проєкт документації [Zudoku](https://zudoku.dev), задеплоєний на GitHub Pages |
| `demo.py` | Демонстраційний скрипт доменної моделі |

## Запуск API

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Усі запити (крім `/docs`, `/openapi.json`) потребують заголовка `X-API-Key: demo-key-123`.

## Документація (Zudoku)

Опубліковано на GitHub Pages: **https://metholyn.github.io/ticketing-system-api/**

Локальний запуск документації:

```bash
cd zudoku-docs
npm install
npm run dev
```

## SDK

Python SDK згенеровано інструментом `openapi-python-client` на основі `openapi.yaml`:

```bash
cd sdk/python-client
pip install .
```

## Автор

Mark Pereverzov
