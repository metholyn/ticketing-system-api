"""Доменні винятки системи продажу квитків."""


class SoldOutError(RuntimeError):
    """Виникає, коли на подію більше немає вільних квитків."""


class InvalidTicketStatusError(RuntimeError):
    """Виникає при недопустимому переході статусу квитка."""
