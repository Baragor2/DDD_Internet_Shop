from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from application.api.exception_handlers import handle_application_exceptions
from logic.queries.categories import GetCategoriesQuery
from application.api.filters import GetFilters
from application.api.categories.schemas import CategoryDetailSchema, CreateCategoryRequestSchema, CreateCategoryResponseSchema, GetCategoriesQueryResponseSchema, PatchCategoryRequestSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.categories import ChangeCategoryTitleCommand, CreateCategoryCommand, DeleteCategoryCommand
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
@handle_application_exceptions
async def create_category_handler(
    schema: CreateCategoryRequestSchema, 
    container: Container = Depends(init_container),
) -> CreateCategoryResponseSchema:
    '''Create new category'''
    mediator: Mediator = container.resolve(Mediator) 
    category, *_ = await mediator.handle_command(CreateCategoryCommand(title=schema.title))
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
@handle_application_exceptions
async def get_categories_handler(
    filters: GetFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetCategoriesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    categories, count = await mediator.handle_query(
        GetCategoriesQuery(filters=filters.to_infra())
    )
    
    return GetCategoriesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[CategoryDetailSchema.from_entity(category) for category in categories],
    )


@router.delete(
    '/{title}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Endpoint deletes a category by oid',
    responses={
        status.HTTP_204_NO_CONTENT: {'model': None},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
@handle_application_exceptions
async def delete_category_handler(
    title: str,
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)
    await mediator.handle_command(
        DeleteCategoryCommand(title=title),
    )
    

@router.patch(
    '/{old_title}',
    response_model=CategoryDetailSchema,
    status_code=status.HTTP_200_OK,
    description="Endpoint changes a category title.",
    responses={
        status.HTTP_200_OK: {'model': CategoryDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def patch_category_title(
    old_title: str,
    schema: PatchCategoryRequestSchema,
    container: Container = Depends(init_container),
) -> CategoryDetailSchema:
    mediator: Mediator = container.resolve(Mediator)
    patched_category, *_ = await mediator.handle_command(
        ChangeCategoryTitleCommand(old_title=old_title, new_title=schema.title),
    )

    return CategoryDetailSchema.from_entity(patched_category)
