from dataclasses import dataclass

from sqlalchemy import insert, select

from domain.entities.users import User
from domain.values.users import Email
from infra.models.users import Users
from infra.repositories.users.base import BaseUsersRepository
from infra.repositories.users.converters import (
    convert_user_entity_to_document,
    convert_user_model_to_entity,
)

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SqlAlchemyUsersRepository(BaseUsersRepository):
    session: AsyncSession

    async def check_user_exists_by_email(self, email: Email) -> bool:
        query = select(Users).where(Users.email == email.as_generic_type())
        result = await self.session.execute(query)
        return bool(result.scalar_one_or_none())

    async def add_user(self, user: User) -> None:
        query = insert(Users).values(convert_user_entity_to_document(user))
        await self.session.execute(query)

    async def get_user_by_email(self, email: Email) -> User:
        query = select(Users).where(Users.email == email.as_generic_type())
        result = await self.session.execute(query)
        return convert_user_model_to_entity(result.scalar_one_or_none())
