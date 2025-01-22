from fastapi import FastAPI

from application.api.categories.handlers import router as categories_router
from application.api.products.handlers import router as products_router
from application.api.users.handlers import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD internet shop",
        docs_url="/api/docs",
        description="DDD internet shop",
        debug=True,
    )

    app.include_router(categories_router, prefix="/categories")
    app.include_router(products_router, prefix="/products")
    app.include_router(users_router, prefix="/users")

    return app
