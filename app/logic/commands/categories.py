from dataclasses import dataclass
from typing import Callable

from domain.entities.categories import Category
from domain.values.categories import CategoryTitle
from infra.unit_of_work import UnitOfWork
from logic.exceptions.categories import CategoryWithThatTitleAlreadyExistsException
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateCategoryCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateCategoryCommandHandler(CommandHandler[CreateCategoryCommand, Category]):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, command: CreateCategoryCommand) -> Category:
        async with self.uow_factory() as uow:
            repo = uow.get_categories_repository()
            
            if await repo.check_category_exists_by_title(command.title):
                raise CategoryWithThatTitleAlreadyExistsException(command.title)
            
            title = CategoryTitle(value=command.title)

            new_category = Category(title=title)

            await repo.add_category(new_category)

            return new_category
