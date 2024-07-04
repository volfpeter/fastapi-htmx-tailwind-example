from datetime import UTC, datetime

from motorhead import ObjectId, UTCDatetime
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """Base model for device events."""

    device_id: ObjectId
    device_code: str
    created_at: UTCDatetime = Field(default_factory=lambda: datetime.now(UTC))
