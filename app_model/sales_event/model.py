from __future__ import annotations

import random
from typing import TYPE_CHECKING, Annotated, Literal, Self

from pydantic import PositiveFloat, StringConstraints

from app_model.event.model import BaseEvent

if TYPE_CHECKING:
    from app_model.device.model import Device

CurrencyCode = Annotated[str, StringConstraints(pattern="^[A-Z]{3}$")]
"""Pydantic currency code type (well, at least in format)."""


class SalesEvent(BaseEvent):
    """Sales event."""

    event_type: Literal["device.sales"] = "device.sales"
    item: str
    price: PositiveFloat
    currency: CurrencyCode

    @classmethod
    def from_device(cls, device: Device) -> Self:
        """Factory that creates a `SalesEvent` for the given device."""
        items = ("espresso", "cortado", "capuccino", "americano")
        currencies: tuple[CurrencyCode, ...] = ("EUR", "USD", "CHF")
        return cls(
            device_id=device.id,
            device_code=device.code,
            item=random.choice(items),  # noqa: S311
            price=round(5 + random.random() * 10, 2),  # noqa: S311
            currency=random.choice(currencies),  # noqa: S311
        )
