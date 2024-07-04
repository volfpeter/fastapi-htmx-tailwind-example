from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fasthx import Jinja, JinjaContext
from jinja2 import Template
from motorhead import AgnosticDatabase, DatabaseProvider, ObjectId
from pydantic import ValidationError
from sse_starlette.sse import EventSourceResponse

from app_model.device.model import Device
from app_model.device.service import DeviceService
from app_model.event.event_source import event_source

from .model import TelemetryEvent


def make_api(*, get_db: DatabaseProvider, jinja: Jinja, prefix: str = "/telemetry-event") -> APIRouter:
    """
    Creates a new API router for telemetry events.

    Arguments:
        get_db: FastAPI dependency that produces a database instance for the API.
        jinja: The Jinja renderer to use.
        prefix: The API prefix to use.
    """
    # -- Constants

    template_prefix = "app_model/telemetry_event"

    table_row_template: Template = jinja.templates.get_template(
        f"{template_prefix}/telemetry-event-table-row.jinja"
    )

    # -- Route dependencies.

    def get_device_service(database: Annotated[AgnosticDatabase, Depends(get_db)]) -> DeviceService:
        return DeviceService(database)

    DependsDeviceService = Annotated[DeviceService, Depends(get_device_service)]

    # -- Routing.

    api = APIRouter(prefix=prefix)

    @api.get("/{device_id}")
    @jinja.hx(f"{template_prefix}/telemetry-events-of-device-dialog.jinja", no_data=True)
    async def telemetry_events_of_device_dialog(
        device_id: ObjectId, device_service: DependsDeviceService
    ) -> Device:
        result = await device_service.get_by_id(device_id)
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(id))

        try:
            return Device.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e

    @api.get("/{device_id}/stream")
    async def stream_by_device_id(
        device_id: ObjectId, device_service: DependsDeviceService, request: Request
    ) -> EventSourceResponse:
        result = await device_service.get_by_id(device_id)
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(id))

        try:
            device = Device.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e

        def encode_event(event: TelemetryEvent) -> str:
            """Converts the given into into HTML for the client."""
            return table_row_template.render(
                request=request, **JinjaContext.unpack_result(route_result=event, route_context={})
            )

        return EventSourceResponse(
            event_source(
                request,
                device,
                make_event=TelemetryEvent.from_device,
                encode_event=encode_event,
                delay=2,
            )
        )

    return api
