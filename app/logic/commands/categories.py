from dataclasses import dataclass

from app.domain.entities.categories import Category
from app.domain.values.categories import CategoryTitle
from app.infra.repositories.categories.base import BaseCategoriesRepository
from app.logic.exceptions.categories import CategoryWithThatTitleAlreadyExistsException
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateCategoryCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateCategoryCommandHandler(CommandHandler[CreateCategoryCommand, Category]):
    categories_repository: BaseCategoriesRepository

    async def handle(self, command: CreateCategoryCommand) -> Category:
        if await self.categories_repository.check_category_exists_by_title(command.title):
            raise CategoryWithThatTitleAlreadyExistsException(command.title)

        title = CategoryTitle(value=command.title)

        new_category = Category.create_category(title=title)

        await self.categories_repository.add_category(new_category)

        return new_category
