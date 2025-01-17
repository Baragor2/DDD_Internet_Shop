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
            
            title = CategoryTitle(value=command.title)
            
            if await categories_repository.check_category_exists_by_title(title):
                raise CategoryWithThatTitleAlreadyExistsException(command.title)
            
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
            
            title = CategoryTitle(value=command.title)
            
            if not await categories_repository.check_category_exists_by_title(title):
                raise CategoryWithThatTitleNotExistsException(command.title)

            await categories_repository.delete_category_by_title(title)


@dataclass(frozen=True)
class ChangeCategoryTitleCommand(BaseCommand):
    old_title: str
    new_title: str


@dataclass(frozen=True)
class ChangeCategoryTitleCommandHandler(CommandHandler[ChangeCategoryTitleCommand, Category]):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, command: ChangeCategoryTitleCommand) -> Category:
        async with self.uow_factory() as uow:
            categories_repository = uow.get_categories_repository()
            
            new_title = CategoryTitle(value=command.new_title)
            old_title = CategoryTitle(value=command.old_title)
            
            if not await categories_repository.check_category_exists_by_title(old_title):
                raise CategoryWithThatTitleNotExistsException(command.old_title)
            
            if await categories_repository.check_category_exists_by_title(new_title):
                raise CategoryWithThatTitleAlreadyExistsException(command.new_title)

            changed_category = await categories_repository.update_category_title(old_title, new_title)

            return changed_category