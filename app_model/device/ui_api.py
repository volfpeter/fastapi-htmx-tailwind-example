from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fasthx import Jinja
from motorhead import AgnosticDatabase, DatabaseProvider, ObjectId
from pydantic import ValidationError

from .model import Device
from .service import DeviceService


def make_api(*, get_db: DatabaseProvider, jinja: Jinja, prefix: str = "/device-ui") -> APIRouter:
    """
    Creates a new API router for device-related HTML-only routes.

    Arguments:
        get_db: FastAPI dependency that produces a database instance for the API.
        jinja: The Jinja renderer to use.
        prefix: The API prefix to use.
    """
    # -- Constants

    template_prefix = "app_model/device"

    # -- Route dependencies.

    def get_service(database: Annotated[AgnosticDatabase, Depends(get_db)]) -> DeviceService:
        return DeviceService(database)

    DependsService = Annotated[DeviceService, Depends(get_service)]

    # -- Routing.

    api = APIRouter(prefix=prefix)

    @api.post("/")
    @jinja.hx(f"{template_prefix}/device-editor-dialog.jinja", no_data=True)
    def new_device_dialog() -> None: ...

    @api.delete("/{id}")
    @jinja.hx(f"{template_prefix}/delete-device-dialog.jinja", no_data=True)
    async def delete_device_dialog(id: ObjectId, service: DependsService) -> Device:
        # Note: fasthx doesn't current support dynamic template selection (multiple templates)
        #     on a given route, which is why this additional route is needed. Otherwise the
        #     `GET /{id}` route could handle this use-case as well.
        #     See this issue: https://github.com/volfpeter/fasthx/issues/17
        result = await service.get_by_id(id)
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(id))

        try:
            return Device.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e

    return api
