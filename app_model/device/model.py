from typing import Literal

from motorhead import BaseDocument, Document, UTCDatetime
from pydantic import Field

DeviceStatus = Literal["idle", "working", "maintenance-required", "error"]
"""Device statuses."""


class HXEventTrigger:
    """Server-side HTMX event triggers (i.e. header names)."""

    after_settle = "HX-Trigger-After-Settle"


class HXDeviceEvent:
    """Server-side, device-related HTMX events."""

    created = "device.created"
    deleted = "device.deleted"
    updated = "device.updated"


class Device(Document):
    """Device database model."""

    code: str = Field(min_length=1)
    location: str
    created_at: UTCDatetime


class DeviceCreate(BaseDocument):
    """Device creation model."""

    code: str = Field(min_length=1)
    location: str


class DeviceUpdate(BaseDocument):
    """Device update model."""

    code: str | None = Field(default=None, min_length=1)
    location: str | None = Field(default=None)
