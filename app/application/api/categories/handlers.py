from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from logic.queries.categories import GetCategoriesQuery
from application.api.filters import GetFilters
from application.api.categories.schemas import CategoryDetailSchema, CreateCategoryRequestSchema, CreateCategoryResponseSchema, DeleteCategoryRequestSchema, GetCategoriesQueryResponseSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.categories import CreateCategoryCommand, DeleteCategoryCommand
from logic.init import init_container
from logic.mediator.base import Mediator


router = APIRouter(
    tags=['Categories'],
)


@router.post(
    '/', 
    response_model=CreateCategoryResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    description='Endpoint creates a new category',
    responses={
        status.HTTP_201_CREATED: {'model': CreateCategoryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_category_handler(
    schema: CreateCategoryRequestSchema, 
    container: Container = Depends(init_container),
) -> CreateCategoryResponseSchema:
    '''Create new category'''
    mediator: Mediator = container.resolve(Mediator) 

    try:
        category, *_ = await mediator.handle_command(CreateCategoryCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message},
        )
    return CreateCategoryResponseSchema.from_entity(category)


@router.get(
    '/',
    response_model=GetCategoriesQueryResponseSchema,
    status_code=status.HTTP_200_OK,
    description='Get information about all categories.',
    responses={
        status.HTTP_200_OK: {'model': GetCategoriesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_categories_handler(
    filters: GetFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetCategoriesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        categories, count = await mediator.handle_query(
            GetCategoriesQuery(filters=filters.to_infra())
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    
    return GetCategoriesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[CategoryDetailSchema.from_entity(category) for category in categories],
    )


@router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Delete category by oid',
    responses={
        status.HTTP_204_NO_CONTENT: {'model': None},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def delete_category_handler(
    schema: DeleteCategoryRequestSchema, 
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    try:
        await mediator.handle_command(
            DeleteCategoryCommand(title=schema.title)
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})