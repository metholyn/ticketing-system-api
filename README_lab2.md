# Lab 2 — Code Documentation (Doxygen)

Domain model of an event ticketing system (variant 14: Event, Ticket),
written in Python.

## Structure

- `app/person.py` — abstract class `Person` and its subclasses `User`, `Organizer` (inheritance)
- `app/venue.py` — the `Venue` class
- `app/event.py` — the `Event` class (depends on `Organizer` and `Venue`)
- `app/ticket.py` — the `Ticket` class and the `TicketStatus` enum (depends on `Event` and `User`)
- `app/repository.py` — the `TicketingRepository` class, aggregating all entities
- `app/exceptions.py` — domain exceptions
- `demo.py` — a demo script that runs the model

## Generating the documentation

The documentation is generated with **Doxygen** (with graphviz for
class UML diagrams and call graphs):

```bash
doxygen Doxyfile
```

The result is in the `docs/html/` folder. Open `docs/html/index.html` in a browser.

## Running the demo

```bash
python3 demo.py
```
