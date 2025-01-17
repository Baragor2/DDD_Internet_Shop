from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable
from uuid import UUID

from domain.entities.products import Characteristic, Product
from domain.values.products import CharacteristicTitle, Description, Price, ProductTitle
from infra.unit_of_work import UnitOfWork
from logic.exceptions.categories import CategoryWithThatOidNotExistsException
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateProductCommand(BaseCommand):
    title: str
    description: str
    price: Decimal
    category_oid: UUID | None
    characteristics: dict[str, Any]



@dataclass(frozen=True)
class CreateProductCommandHandler(CommandHandler[CreateProductCommand, Product]):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, command: CreateProductCommand) -> Product:
        async with self.uow_factory() as uow:
            products_repository = await uow.get_products_repository()
            categories_repository = await uow.get_categories_repository()
            
            if not await categories_repository.check_category_exists_by_oid(command.category_oid):
                raise CategoryWithThatOidNotExistsException(command.category_oid)
            
            new_product = await self.__create_product_entity_from_command(command=command)

            await products_repository.add_product(new_product)

            return new_product


    async def __create_product_entity_from_command(self, command: CreateProductCommand) -> Product:
        product_title = ProductTitle(value=command.title)
        description = Description(value=command.description)
        price = Price(value=command.price)
        characteristics = {
            CharacteristicTitle(value=title): value
            for title, value in command.characteristics.items()
        }

        new_product = Product.create_product(
            title=product_title,
            description=description,
            price=price,
            image_oid=None,
            category_oid=command.category_oid,
            characteristics=characteristics,
        )

        return new_product
