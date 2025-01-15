from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from logic.init import init_container
from application.api.categories.handlers import router as categories_router

def create_app() -> FastAPI:
    app = FastAPI(
        title='FastAPIChat',
        docs_url='/api/docs',
        description='FastAPI DDD Chat',
        debug=True,
    )

    app.include_router(categories_router, prefix="/categories")

    return app
