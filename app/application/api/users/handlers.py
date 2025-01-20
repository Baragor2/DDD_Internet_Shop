from fastapi import APIRouter, Depends, Response, status
from punq import Container

from logic.auth import Auth
from logic.commands.users import CreateUserCommand, LoginUserCommand
from logic.mediator.base import Mediator
from application.api.schemas import ErrorSchema
from logic.init import init_container
from application.api.exception_handlers import handle_application_exceptions
from application.api.users.schemas import CreateUserRequestSchema, CreateUserResponseSchema, LoginUserRequestSchema

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


@router.post(
    '/login', 
    status_code=status.HTTP_200_OK,
    description='Endpoint logins a user',
    responses={
        status.HTTP_200_OK: {'model': None},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
@handle_application_exceptions
async def login_user(
    response: Response,
    schema: LoginUserRequestSchema,
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator) 
    auth: Auth = container.resolve(Auth)

    user, *_ = await mediator.handle_command(
        LoginUserCommand(
            email=schema.email,
            password=schema.password,
        )
    )

    access_token = await auth.create_access_token({"sub": user.username.as_generic_type()})
    response.set_cookie("internet_shop_access_token", access_token, httponly=True)
