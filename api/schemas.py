"""Pydantic request/response schemas for the Ticketing System REST API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.ticket import TicketStatus


# ---------------------------------------------------------------- Organizer
class OrganizerCreate(BaseModel):
    full_name: str = Field(..., examples=["Olena Shevchenko"])
    email: EmailStr = Field(..., examples=["olena@eventpro.ua"])
    organization_name: str = Field("", examples=["EventPro"])


class OrganizerOut(OrganizerCreate):
    person_id: int = Field(..., examples=[1])


# --------------------------------------------------------------------- Venue
class VenueCreate(BaseModel):
    name: str = Field(..., examples=["Palace Ukraina"])
    address: str = Field(..., examples=["Kyiv, Velyka Vasylkivska 103"])
    capacity: int = Field(..., gt=0, examples=[2000])


class VenueOut(VenueCreate):
    venue_id: int = Field(..., examples=[1])


# ---------------------------------------------------------------------- User
class UserCreate(BaseModel):
    full_name: str = Field(..., examples=["Mark Pereverzov"])
    email: EmailStr = Field(..., examples=["mark@example.com"])
    phone: str = Field("", examples=["+380501234567"])


class UserOut(UserCreate):
    person_id: int = Field(..., examples=[1])
    ticket_count: int = Field(0, examples=[2])


# --------------------------------------------------------------------- Event
class EventCreate(BaseModel):
    title: str = Field(..., examples=["Tech Conference 2026"])
    start_time: datetime = Field(..., examples=["2026-12-01T10:00:00"])
    organizer_id: int = Field(..., examples=[1])
    venue_id: int = Field(..., examples=[1])
    ticket_price: float = Field(..., gt=0, examples=[25.0])
    total_tickets: int = Field(..., gt=0, examples=[200])


class EventUpdate(BaseModel):
    title: str | None = Field(None, examples=["Tech Conference 2026 (updated)"])
    start_time: datetime | None = None
    ticket_price: float | None = Field(None, gt=0)
    total_tickets: int | None = Field(None, gt=0)


class EventOut(BaseModel):
    event_id: int = Field(..., examples=[1])
    title: str
    start_time: datetime
    organizer_id: int
    venue_id: int
    ticket_price: float
    total_tickets: int
    sold_tickets: int
    available_tickets: int


# -------------------------------------------------------------------- Ticket
class TicketCreate(BaseModel):
    event_id: int = Field(..., examples=[1])
    user_id: int = Field(..., examples=[1])
    seat_number: str = Field(..., examples=["A1"])


class TicketUpdate(BaseModel):
    status: TicketStatus = Field(..., examples=[TicketStatus.PAID])


class TicketOut(BaseModel):
    ticket_id: int = Field(..., examples=[1])
    event_id: int
    user_id: int
    seat_number: str
    status: TicketStatus
    purchase_time: datetime


class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["Event not found"])
