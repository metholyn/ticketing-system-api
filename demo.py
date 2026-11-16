"""Демонстраційний скрипт роботи доменної моделі Ticketing system.

Запуск: python demo.py
"""

from datetime import datetime

from app.repository import TicketingRepository


def main() -> None:
    repo = TicketingRepository()

    organizer = repo.add_organizer(
        full_name="Olena Shevchenko",
        email="olena@eventpro.ua",
        organization_name="EventPro",
    )
    venue = repo.add_venue(name="Palace Ukraina", address="Kyiv, Velyka Vasylkivska 103", capacity=200)
    event = repo.add_event(
        title="Tech Conference 2026",
        start_time=datetime(2026, 12, 1, 10, 0),
        organizer_id=organizer.person_id,
        venue_id=venue.venue_id,
        ticket_price=25.0,
        total_tickets=2,
    )

    user = repo.add_user(full_name="Mark Pereverzov", email="mark@example.com")

    ticket = repo.add_ticket(event_id=event.event_id, user_id=user.person_id, seat_number="A1")
    ticket.pay()

    print(f"Organizer: {organizer}")
    print(f"Event: {event.title} at {event.venue.name}, available: {event.available_tickets}")
    print(f"Ticket #{ticket.ticket_id} status: {ticket.status}")


if __name__ == "__main__":
    main()
