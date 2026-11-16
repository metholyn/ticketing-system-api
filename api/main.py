"""REST API системи продажу квитків на події (Ticketing System).

Варіант 14: сутності Event, Ticket. Для роботи цих сутностей також
реалізовано допоміжні ресурси Organizer, Venue, User (вони потрібні
як зовнішні ключі для Event та Ticket).

Запуск локально:
    uvicorn api.main:app --reload

OpenAPI-специфікація доступна за адресами:
    GET /openapi.json
    GET /docs   (Swagger UI)
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.exceptions import InvalidTicketStatusError, SoldOutError
from app.repository import TicketingRepository
from api.schemas import (
    ErrorResponse,
    EventCreate,
    EventOut,
    EventUpdate,
    OrganizerCreate,
    OrganizerOut,
    TicketCreate,
    TicketOut,
    TicketUpdate,
    UserCreate,
    UserOut,
    VenueCreate,
    VenueOut,
)

#: Статичний набір дійсних демонстраційних API-ключів.
#: У продакшн-системі ключі зберігались би в базі даних/секрет-сховищі.
_VALID_API_KEYS = {"demo-key-123"}

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(api_key: str | None = Security(_api_key_header)) -> str:
    """Перевіряє наявність та коректність API-ключа в заголовку X-API-Key.

    Raises:
        HTTPException: 401, якщо ключ відсутній або невірний.
    """
    if api_key is None or api_key not in _VALID_API_KEYS:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key. Pass it in the 'X-API-Key' header.",
        )
    return api_key


app = FastAPI(
    title="Ticketing System API",
    description=(
        "REST API для системи продажу квитків на події. "
        "Основні сутності: **Event** (подія) та **Ticket** (квиток). "
        "Усі запити потребують заголовка `X-API-Key`."
    ),
    version="1.0.0",
    contact={"name": "Mark Pereverzov"},
    dependencies=[Depends(require_api_key)],
)

repo = TicketingRepository()


def _event_out(event) -> EventOut:
    return EventOut(
        event_id=event.event_id,
        title=event.title,
        start_time=event.start_time,
        organizer_id=event.organizer.person_id,
        venue_id=event.venue.venue_id,
        ticket_price=event.ticket_price,
        total_tickets=event.total_tickets,
        sold_tickets=event.sold_tickets,
        available_tickets=event.available_tickets,
    )


def _ticket_out(ticket) -> TicketOut:
    return TicketOut(
        ticket_id=ticket.ticket_id,
        event_id=ticket.event.event_id,
        user_id=ticket.owner.person_id,
        seat_number=ticket.seat_number,
        status=ticket.status,
        purchase_time=ticket.purchase_time,
    )


# ------------------------------------------------------------- Organizers
@app.post(
    "/organizers",
    response_model=OrganizerOut,
    status_code=status.HTTP_201_CREATED,
    tags=["organizers"],
    summary="Створити організатора",
)
def create_organizer(payload: OrganizerCreate) -> OrganizerOut:
    organizer = repo.add_organizer(
        full_name=payload.full_name,
        email=payload.email,
        organization_name=payload.organization_name,
    )
    return OrganizerOut(**payload.model_dump(), person_id=organizer.person_id)


@app.get("/organizers", response_model=list[OrganizerOut], tags=["organizers"])
def list_organizers() -> list[OrganizerOut]:
    return [
        OrganizerOut(
            person_id=o.person_id,
            full_name=o.full_name,
            email=o.email,
            organization_name=o.organization_name,
        )
        for o in repo._organizers.values()
    ]


@app.get(
    "/organizers/{organizer_id}",
    response_model=OrganizerOut,
    responses={404: {"model": ErrorResponse}},
    tags=["organizers"],
)
def get_organizer(organizer_id: int) -> OrganizerOut:
    organizer = repo.get_organizer(organizer_id)
    if organizer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Organizer not found")
    return OrganizerOut(
        person_id=organizer.person_id,
        full_name=organizer.full_name,
        email=organizer.email,
        organization_name=organizer.organization_name,
    )


# ------------------------------------------------------------------ Venues
@app.post(
    "/venues",
    response_model=VenueOut,
    status_code=status.HTTP_201_CREATED,
    tags=["venues"],
    summary="Створити майданчик",
)
def create_venue(payload: VenueCreate) -> VenueOut:
    venue = repo.add_venue(name=payload.name, address=payload.address, capacity=payload.capacity)
    return VenueOut(**payload.model_dump(), venue_id=venue.venue_id)


@app.get("/venues", response_model=list[VenueOut], tags=["venues"])
def list_venues() -> list[VenueOut]:
    return [
        VenueOut(venue_id=v.venue_id, name=v.name, address=v.address, capacity=v.capacity)
        for v in repo._venues.values()
    ]


@app.get(
    "/venues/{venue_id}",
    response_model=VenueOut,
    responses={404: {"model": ErrorResponse}},
    tags=["venues"],
)
def get_venue(venue_id: int) -> VenueOut:
    venue = repo.get_venue(venue_id)
    if venue is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Venue not found")
    return VenueOut(venue_id=venue.venue_id, name=venue.name, address=venue.address, capacity=venue.capacity)


# ------------------------------------------------------------------- Users
@app.post(
    "/users",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
    summary="Зареєструвати користувача",
)
def create_user(payload: UserCreate) -> UserOut:
    user = repo.add_user(full_name=payload.full_name, email=payload.email, phone=payload.phone)
    return UserOut(**payload.model_dump(), person_id=user.person_id, ticket_count=0)


@app.get("/users", response_model=list[UserOut], tags=["users"])
def list_users() -> list[UserOut]:
    return [
        UserOut(
            person_id=u.person_id,
            full_name=u.full_name,
            email=u.email,
            phone=u.phone,
            ticket_count=u.ticket_count(),
        )
        for u in repo.list_users()
    ]


@app.get(
    "/users/{user_id}",
    response_model=UserOut,
    responses={404: {"model": ErrorResponse}},
    tags=["users"],
)
def get_user(user_id: int) -> UserOut:
    user = repo.get_user(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(
        person_id=user.person_id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        ticket_count=user.ticket_count(),
    )


# ------------------------------------------------------------------- Events
@app.post(
    "/events",
    response_model=EventOut,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ErrorResponse}},
    tags=["events"],
    summary="Створити подію",
)
def create_event(payload: EventCreate) -> EventOut:
    try:
        event = repo.add_event(
            title=payload.title,
            start_time=payload.start_time,
            organizer_id=payload.organizer_id,
            venue_id=payload.venue_id,
            ticket_price=payload.ticket_price,
            total_tickets=payload.total_tickets,
        )
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Organizer or venue not found: {exc}")
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return _event_out(event)


@app.get("/events", response_model=list[EventOut], tags=["events"], summary="Список подій")
def list_events() -> list[EventOut]:
    return [_event_out(e) for e in repo.list_events()]


@app.get(
    "/events/{event_id}",
    response_model=EventOut,
    responses={404: {"model": ErrorResponse}},
    tags=["events"],
    summary="Отримати подію за id",
)
def get_event(event_id: int) -> EventOut:
    event = repo.get_event(event_id)
    if event is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Event not found")
    return _event_out(event)


@app.put(
    "/events/{event_id}",
    response_model=EventOut,
    responses={404: {"model": ErrorResponse}},
    tags=["events"],
    summary="Оновити подію",
)
def update_event(event_id: int, payload: EventUpdate) -> EventOut:
    event = repo.get_event(event_id)
    if event is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Event not found")
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(event, field, value)
    return _event_out(event)


@app.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
    tags=["events"],
    summary="Видалити подію",
)
def delete_event(event_id: int) -> None:
    if repo.get_event(event_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Event not found")
    repo.delete_event(event_id)


# ------------------------------------------------------------------ Tickets
@app.post(
    "/tickets",
    response_model=TicketOut,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
    tags=["tickets"],
    summary="Придбати (створити) квиток",
)
def create_ticket(payload: TicketCreate) -> TicketOut:
    try:
        ticket = repo.add_ticket(
            event_id=payload.event_id, user_id=payload.user_id, seat_number=payload.seat_number
        )
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Event or user not found: {exc}")
    except SoldOutError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc))
    return _ticket_out(ticket)


@app.get("/tickets", response_model=list[TicketOut], tags=["tickets"], summary="Список квитків")
def list_tickets() -> list[TicketOut]:
    return [_ticket_out(t) for t in repo.list_tickets()]


@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketOut,
    responses={404: {"model": ErrorResponse}},
    tags=["tickets"],
    summary="Отримати квиток за id",
)
def get_ticket(ticket_id: int) -> TicketOut:
    ticket = repo.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return _ticket_out(ticket)


@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketOut,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
    tags=["tickets"],
    summary="Змінити статус квитка (pay/cancel)",
)
def update_ticket(ticket_id: int, payload: TicketUpdate) -> TicketOut:
    ticket = repo.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    try:
        if payload.status.value == "paid":
            ticket.pay()
        elif payload.status.value == "cancelled":
            ticket.cancel()
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Unsupported target status")
    except InvalidTicketStatusError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc))
    return _ticket_out(ticket)


@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
    tags=["tickets"],
    summary="Скасувати та видалити квиток",
)
def delete_ticket(ticket_id: int) -> None:
    if repo.get_ticket(ticket_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    repo.delete_ticket(ticket_id)
