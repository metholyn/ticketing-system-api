from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.ticket_out import TicketOut
from ...models.ticket_update import TicketUpdate
from ...types import Response


def _get_kwargs(
    ticket_id: int,
    *,
    body: TicketUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/tickets/{ticket_id}".format(
            ticket_id=quote(str(ticket_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> ErrorResponse | HTTPValidationError | TicketOut | None:
    if response.status_code == 200:
        response_200 = TicketOut.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[ErrorResponse | HTTPValidationError | TicketOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    body: TicketUpdate,
) -> Response[ErrorResponse | HTTPValidationError | TicketOut]:
    """Змінити статус квитка (pay/cancel)

    Args:
        ticket_id (int):
        body (TicketUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | TicketOut]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    body: TicketUpdate,
) -> ErrorResponse | HTTPValidationError | TicketOut | None:
    """Змінити статус квитка (pay/cancel)

    Args:
        ticket_id (int):
        body (TicketUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | TicketOut
    """

    return sync_detailed(
        ticket_id=ticket_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    body: TicketUpdate,
) -> Response[ErrorResponse | HTTPValidationError | TicketOut]:
    """Змінити статус квитка (pay/cancel)

    Args:
        ticket_id (int):
        body (TicketUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | TicketOut]
    """

    kwargs = _get_kwargs(
        ticket_id=ticket_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticket_id: int,
    *,
    client: AuthenticatedClient,
    body: TicketUpdate,
) -> ErrorResponse | HTTPValidationError | TicketOut | None:
    """Змінити статус квитка (pay/cancel)

    Args:
        ticket_id (int):
        body (TicketUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | TicketOut
    """

    return (
        await asyncio_detailed(
            ticket_id=ticket_id,
            client=client,
            body=body,
        )
    ).parsed
