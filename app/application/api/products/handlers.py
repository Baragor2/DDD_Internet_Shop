from fastapi import APIRouter, Depends, status
from punq import Container

from logic.queries.products import GetProductsQuery
from application.api.filters import GetFilters
from logic.commands.products import CreateProductCommand
from application.api.exception_handlers import handle_application_exceptions
from application.api.products.schemas import (
    CreateProductRequestSchema,
    CreateProductResponseSchema,
    GetProductsQueryResponseSchema,
    ProductDetailSchema,
)
from application.api.schemas import ErrorSchema
from logic.init import init_container
from logic.mediator.base import Mediator


router = APIRouter(
    tags=["Products"],
)


@router.post(
    "/",
    response_model=CreateProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates a new product",
    responses={
        status.HTTP_201_CREATED: {"model": CreateProductResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@handle_application_exceptions
async def create_product_handler(
    schema: CreateProductRequestSchema,
    container: Container = Depends(init_container),
) -> CreateProductResponseSchema:
    """Create new product"""
    mediator: Mediator = container.resolve(Mediator)
    product, *_ = await mediator.handle_command(
        CreateProductCommand(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            category_oid=schema.category_oid,
            characteristics=schema.characteristics,
        )
    )
    return CreateProductResponseSchema.from_entity(product)


@router.get(
    "/",
    response_model=GetProductsQueryResponseSchema,
    status_code=status.HTTP_200_OK,
    description="Get information about all products.",
    responses={
        status.HTTP_200_OK: {"model": GetProductsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
@handle_application_exceptions
async def get_categories_handler(
    filters: GetFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetProductsQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    products, count = await mediator.handle_query(
        GetProductsQuery(filters=filters.to_infra())
    )

    return GetProductsQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ProductDetailSchema.from_entity(product) for product in products],
    )
