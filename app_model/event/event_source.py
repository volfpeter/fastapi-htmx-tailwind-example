import asyncio
from collections.abc import AsyncGenerator, Callable
from typing import TypeVar

from fastapi import Request
from pydantic import BaseModel

_TItem = TypeVar("_TItem")
_TEvent = TypeVar("_TEvent", bound=BaseModel)


async def event_source(
    request: Request,
    item: _TItem,
    *,
    make_event: Callable[[_TItem], _TEvent],
    encode_event: Callable[[_TEvent], str],
    delay: float = 0.5,
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields (encoded) events for the given item.

    Arguments:
        request: The request that triggered the event source.
        item: The item events should be generated for.
        make_event: Factory that creates the event.
        encode_event: Encoder that turns events into their string representation.
        delay: Time between events (in seconds).
    """
    while True:
        if await request.is_disconnected():
            break

        await asyncio.sleep(delay)
        yield encode_event(make_event(item))
