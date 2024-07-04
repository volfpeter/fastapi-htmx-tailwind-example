import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motorhead import AgnosticDatabase


async def _create_demo_data(db: AgnosticDatabase) -> None:
    """Creates some data for the application."""
    from app_model.device.model import DeviceCreate
    from app_model.device.service import DeviceService

    svc = DeviceService(db)
    for code, location in (
        ("coffee-machine-4", "ams-office-1-floor-1"),
        ("espresso-13", "bud-office"),
        ("barista-1-37", "remote"),
    ):
        await svc.create(DeviceCreate(code=code, location=location))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from app_model.config import create_indexes

    from .database import get_database

    db = get_database()

    # Create all indexes on startup if they don't exist already.
    await create_indexes(db)

    if create_data := os.environ.get("CREATE_DEMO_DATA", None):
        if create_data.lower() in {"1", "true", "y", "yes"}:
            await _create_demo_data(db)

    yield  # Application starts
