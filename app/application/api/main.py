from fastapi import FastAPI

from application.api.categories.handlers import router as categories_router
from application.api.products.handlers import router as products_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='FastAPIChat',
        docs_url='/api/docs',
        description='FastAPI DDD Chat',
        debug=True,
    )

    app.include_router(categories_router, prefix="/categories")
    app.include_router(products_router, prefix='/products')

    return app
