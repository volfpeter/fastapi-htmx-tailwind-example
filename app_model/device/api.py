from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fasthx import Jinja
from motorhead import AgnosticDatabase, DatabaseProvider, DeleteError, DeleteResultModel, ObjectId
from pydantic import ValidationError

from .model import Device, DeviceCreate, DeviceUpdate, HXDeviceEvent, HXEventTrigger
from .service import DeviceService


def make_api(*, get_db: DatabaseProvider, jinja: Jinja, prefix: str = "/device") -> APIRouter:  # noqa: C901
    """
    Creates a new API router for interacting with devices.

    Notes:
        - BSON to `Device` conversion is bad for performance, but it makes the templates cleaner.

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

    @api.get("/")
    @jinja.hx(f"{template_prefix}/devices-table.jinja")
    async def get_all(service: DependsService, code: str | None = None) -> list[Device]:
        try:
            query = None if code is None else {"code": {"$regex": code}}  # Basic substring search.
            return [Device.model_validate(d) async for d in service.find(query).sort({"code": 1})]
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e

    @api.post("/")
    async def create(data: DeviceCreate, service: DependsService, response: Response) -> Device:
        try:
            result = await service.create(data)
            response.headers[HXEventTrigger.after_settle] = HXDeviceEvent.created
            return Device.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Creation failed.") from e

    @api.get("/{id}")
    @jinja.hx(f"{template_prefix}/device-editor-dialog.jinja")
    async def get_by_id(id: ObjectId, service: DependsService) -> Device:
        result = await service.get_by_id(id)
        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(id))

        try:
            return Device.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e

    @api.patch("/{id}")
    async def update_by_id(
        id: ObjectId,
        data: DeviceUpdate,
        service: DependsService,
        response: Response,
    ) -> Device:
        try:
            result = await service.update(id, data)
            response.headers[HXEventTrigger.after_settle] = HXDeviceEvent.updated
            return Device.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Schema mismatch") from e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(id)) from e

    @api.delete("/{id}", response_model=DeleteResultModel)
    async def delete_by_id(id: ObjectId, service: DependsService, response: Response) -> DeleteResultModel:
        try:
            result = await service.delete_by_id(id)
            response.headers[HXEventTrigger.after_settle] = HXDeviceEvent.deleted
        except DeleteError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(id)) from e
        if result.deleted_count == 0:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(id))

        return DeleteResultModel(delete_count=result.deleted_count)

    return api
