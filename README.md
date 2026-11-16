# Ticketing System API

A university project: a REST API for an event ticketing system (variant 14:
`Event`, `Ticket` entities). Built for the "code documentation" and "API
documentation" practical assignments.

## Repository structure

| Path | Description |
| --- | --- |
| `app/` | Domain model (Person → User/Organizer, Venue, Event, Ticket) |
| `api/` | REST API built with FastAPI (CRUD for Event, Ticket and the auxiliary resources) |
| `openapi.yaml`, `openapi.json` | OpenAPI 3.1 specification, generated from the code |
| `sdk/python-client/` | Python SDK client generated with `openapi-python-client` |
| `zudoku-docs/` | [Zudoku](https://zudoku.dev) documentation project, deployed to GitHub Pages |
| `demo.py` | Demo script for the domain model |

## Running the API

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Every request (except `/docs`, `/openapi.json`) requires the header
`X-API-Key: demo-key-123`.

## Documentation (Zudoku)

Published on GitHub Pages: **https://metholyn.github.io/ticketing-system-api/**

Running the docs locally:

```bash
cd zudoku-docs
npm install
npm run dev
```

## SDK

The Python SDK is generated with `openapi-python-client` from `openapi.yaml`:

```bash
cd sdk/python-client
pip install .
```

## Author

Mark Pereverzov
