from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from logic.init import init_container
from settings.config import Config

from punq import Container


def create_app() -> FastAPI:
    app = FastAPI(
        title='FastAPIChat',
        docs_url='/api/docs',
        description='FastAPI DDD Chat',
        debug=True,
    )

    return app
