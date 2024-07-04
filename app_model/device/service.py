from datetime import UTC, datetime
from typing import Any

from motorhead import IndexData, Service

from .model import DeviceCreate, DeviceUpdate


class DeviceService(Service[DeviceCreate, DeviceUpdate]):
    """Database service for interacting with devices."""

    __slots__ = ()

    collection_name = "devices"

    indexes = {
        "unique-code": IndexData(
            keys="code",
            unique=True,
            collation={"locale": "en", "strength": 1},
        )
    }

    async def _convert_for_insert(self, data: DeviceCreate) -> dict[str, Any]:
        return {
            **(await super()._convert_for_insert(data)),
            "created_at": datetime.now(UTC),  # Automatically add the creation date.
        }
