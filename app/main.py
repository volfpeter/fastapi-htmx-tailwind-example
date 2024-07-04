from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def make_app() -> FastAPI:
    from .api import register_routes
    from .database import get_database
    from .jinja import jinja
    from .lifespan import lifespan

    app = FastAPI(lifespan=lifespan)

    app.mount("/static", StaticFiles(directory="static"), name="static")

    register_routes(app, get_db=get_database, jinja=jinja)

    return app
