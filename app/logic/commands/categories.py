from dataclasses import dataclass
from typing import Callable
from uuid import UUID

from domain.entities.categories import Category
from domain.values.categories import CategoryTitle
from infra.unit_of_work import UnitOfWork
from logic.exceptions.categories import CategoryWithThatTitleAlreadyExistsException, CategoryWithThatTitleNotExistsException
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateCategoryCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateCategoryCommandHandler(CommandHandler[CreateCategoryCommand, Category]):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, command: CreateCategoryCommand) -> Category:
        async with self.uow_factory() as uow:
            categories_repository = uow.get_categories_repository()
            
            if await categories_repository.check_category_exists_by_title(command.title):
                raise CategoryWithThatTitleAlreadyExistsException(command.title)
            
            title = CategoryTitle(value=command.title)

            new_category = Category(title=title)

            await categories_repository.add_category(new_category)

            return new_category


@dataclass(frozen=True)
class DeleteCategoryCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class DeleteCategoryCommandHandler(CommandHandler[DeleteCategoryCommand, Category]):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, command: DeleteCategoryCommand) -> None:
        async with self.uow_factory() as uow:
            categories_repository = uow.get_categories_repository()
            
            if not await categories_repository.check_category_exists_by_title(command.title):
                raise CategoryWithThatTitleNotExistsException(command.title)
            
            await categories_repository.delete_category_by_title(command.title)
