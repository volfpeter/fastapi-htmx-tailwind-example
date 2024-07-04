from __future__ import annotations

import random
import re
from typing import TYPE_CHECKING, Literal, Self

from app_model.event.model import BaseEvent

if TYPE_CHECKING:
    from app_model.device.model import Device

DeviceStatus = Literal["idle", "working", "maintenance-required", "error"]
"""Device statuses."""

_detail_corpus = re.sub(
    "[., ]+",
    " ",
    (
        "Cortado organic extra  steamed, sit extra , "
        "crema, aromatic instant, black bar  est caramelization aroma "
        "white medium and plunger pot. So beans, spoon, aroma, brewed "
        "dripper arabica, coffee, robust coffee extra  macchiato espresso "
        "cinnamon. Cappuccino sugar robusta qui, filter ut pumpkin spice, "
        "and trifecta acerbic chicory blue mountain cinnamon siphon. "
        "Strong, organic grinder carajillo qui, robusta sweet coffee "
        "crema plunger pot sugar cream instant cortado. Cortado irish "
        "acerbic, variety, roast wings fair trade whipped half and half, "
        "ut lungo that ristretto skinny redeye beans cinnamon. Carajillo "
        "to go affogato pumpkin spice single shot, milk ristretto, siphon "
        "and decaffeinated iced and, sit viennese, con panna caramelization "
        "mocha grinder organic saucer. Grinder ut siphon barista variety "
        "body that saucer strong americano java cup brewed. French press "
        "ristretto redeye wings arabica shop aged milk galão milk, iced "
        "coffee instant crema aged steamed mazagran. Café au lait cup "
        "foam aroma et, variety as bar  ristretto barista id organic "
        "skinny et so iced bar  a fair trade turkish. Cappuccino bar "
        "flavour, as, siphon, con panna trifecta instant ristretto aroma "
        "as acerbic turkish saucer."
    ).lower(),
).split()


class TelemetryEvent(BaseEvent):
    """Telemetry event."""

    event_type: Literal["device.telemetry"] = "device.telemetry"
    status: DeviceStatus
    detail: str

    @classmethod
    def from_device(cls, device: Device) -> Self:
        """Factory that creates a `TelemetryEvent` for the given device."""
        device_statuses: tuple[DeviceStatus, ...] = ("idle", "working", "maintenance-required", "error")
        device_status_weights = (10, 3, 1, 1)
        return cls(
            device_id=device.id,
            device_code=device.code,
            status=random.choices(device_statuses, device_status_weights)[0],  # noqa: S311
            detail=" ".join(random.choices(_detail_corpus, k=5)).capitalize(),  # noqa: S311
        )
