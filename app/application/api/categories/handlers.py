from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from app.application.api.categories.schemas import CreateCategoryRequestSchema, CreateCategoryResponseSchema
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.logic.commands.categories import CreateCategoryCommand
from app.logic.init import init_container
from app.logic.mediator.base import Mediator


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
    container: Container = Depends(init_container)
) -> CreateCategoryResponseSchema:
    '''Create new category'''
    mediator: Mediator = container.resolve(Mediator) 

    try:
        chat, *_ = await mediator.handle_command(CreateCategoryCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message},
        )
    return CreateCategoryResponseSchema.from_entity(chat)
