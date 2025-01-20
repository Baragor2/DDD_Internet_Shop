from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from logic.commands.users import CreateUserCommand
from logic.mediator.base import Mediator
from application.api.schemas import ErrorSchema
from logic.init import init_container
from application.api.exception_handlers import handle_application_exceptions
from application.api.users.schemas import CreateUserRequestSchema, CreateUserResponseSchema

router = APIRouter()


@router.post(
    '/', 
    response_model=CreateUserResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    description='Endpoint registers a new user',
    responses={
        status.HTTP_201_CREATED: {'model': CreateUserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
@handle_application_exceptions
async def register_user(
    schema: CreateUserRequestSchema,
    container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator) 
    user, *_ = await mediator.handle_command(
        CreateUserCommand(
            username=schema.username,
            email=schema.email,
            password=schema.password,
        )
    )
    return CreateUserResponseSchema.from_entity(user)
