from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx2

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.venue_out import VenueOut
from ...types import Response


def _get_kwargs(
    venue_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/venues/{venue_id}".format(
            venue_id=quote(str(venue_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> ErrorResponse | HTTPValidationError | VenueOut | None:
    if response.status_code == 200:
        response_200 = VenueOut.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx2.Response
) -> Response[ErrorResponse | HTTPValidationError | VenueOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    venue_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | HTTPValidationError | VenueOut]:
    """Get Venue

    Args:
        venue_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | VenueOut]
    """

    kwargs = _get_kwargs(
        venue_id=venue_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    venue_id: int,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | HTTPValidationError | VenueOut | None:
    """Get Venue

    Args:
        venue_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | VenueOut
    """

    return sync_detailed(
        venue_id=venue_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    venue_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | HTTPValidationError | VenueOut]:
    """Get Venue

    Args:
        venue_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | VenueOut]
    """

    kwargs = _get_kwargs(
        venue_id=venue_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    venue_id: int,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | HTTPValidationError | VenueOut | None:
    """Get Venue

    Args:
        venue_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | VenueOut
    """

    return (
        await asyncio_detailed(
            venue_id=venue_id,
            client=client,
        )
    ).parsed
