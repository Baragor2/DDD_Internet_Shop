from dataclasses import dataclass
from typing import Any, Callable
from uuid import UUID, uuid4


from logic.auth import Auth
from domain.entities.carts import Cart
from logic.exceptions.users import IncorrectEmailOrPasswordException, UserWithThatEmailAlreadyExistsException
from domain.entities.users import Role, User
from domain.values.users import Email, UserName, UserRole
from infra.unit_of_work import UnitOfWork
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    uow_factory: Callable[[], UnitOfWork]
    auth: Auth

    async def handle(self, command: CreateUserCommand) -> User:
        async with self.uow_factory() as uow:            
            users_repository = await uow.get_users_repository()
            carts_repository = await uow.get_carts_repository()

            email = Email(command.email)

            if await users_repository.check_user_exists_by_email(email):
                raise UserWithThatEmailAlreadyExistsException(command.email)
            
            new_cart = Cart.create_cart()
            new_user = await self.__create_entity_from_command(command, new_cart.oid)

            await carts_repository.add_cart(new_cart)
            await users_repository.add_user(new_user)

            return new_user
        
    async def __create_entity_from_command(self, command: CreateUserCommand, cart_oid: UUID) -> User:
        username = UserName(command.username)
        email = Email(command.email)
        password_hash = await self.auth.get_password_hash(command.password)
        role = Role(UserRole("User"))

        return User.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            cart_oid=cart_oid,
        )


@dataclass(frozen=True)
class LoginUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserCommandHandler(CommandHandler[LoginUserCommand, User]):
    uow_factory: Callable[[], UnitOfWork]
    auth: Auth

    async def handle(self, command: LoginUserCommand) -> User:
        async with self.uow_factory() as uow:            
            users_repository = await uow.get_users_repository()

            email = Email(command.email)

            if not await users_repository.check_user_exists_by_email(email):
                raise IncorrectEmailOrPasswordException()
            
            user = await users_repository.get_user_by_email(email)

            if not await self.auth.validate_password(command.password, user.password_hash):
                raise IncorrectEmailOrPasswordException()
            
            return user