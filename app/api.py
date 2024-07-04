from fastapi import FastAPI
from fasthx import Jinja
from motorhead import DatabaseProvider

from app_model.device.api import make_api as make_device_api
from app_model.device.ui_api import make_api as make_device_ui_api
from app_model.sales_event.api import make_api as make_sales_api
from app_model.telemetry_event.api import make_api as make_telemetry_api


def _register_main_pages(app: FastAPI, *, jinja: Jinja) -> None:
    @app.get("/", include_in_schema=False)
    @jinja.page("app_model/device/devices.jinja")
    def index() -> list[None]:
        return []


def _register_utility_routes(app: FastAPI) -> None:
    @app.get("/ack", response_model=None, include_in_schema=False)
    def ack() -> None:
        # HTMX has no built-in way to trigger changes without making a request.
        # There are various workarounds, but for simplicity (and to avoid additional
        # dependencies), this route can be called when no server-side action is needed.
        # The response code should be 204 for this kind of route, but that also doesn't
        # trigger the HTMX action in the client, so the default 200 is used instead
        ...


def register_routes(app: FastAPI, *, get_db: DatabaseProvider, jinja: Jinja) -> None:
    app.include_router(make_device_api(get_db=get_db, jinja=jinja))
    app.include_router(make_device_ui_api(get_db=get_db, jinja=jinja), include_in_schema=False)
    app.include_router(make_sales_api(get_db=get_db, jinja=jinja), include_in_schema=False)
    app.include_router(make_telemetry_api(get_db=get_db, jinja=jinja), include_in_schema=False)

    _register_main_pages(app, jinja=jinja)
    _register_utility_routes(app)
