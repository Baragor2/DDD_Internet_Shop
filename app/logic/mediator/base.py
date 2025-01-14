from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from logic.commands.base import CR, CT, BaseCommand, CommandHandler
from logic.exceptions.mediator import CommandHandlersNotRegisteredException
from logic.mediator.command import CommandMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(eq=False)
class Mediator(QueryMediator, CommandMediator):
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        self.queries_map[query] = query_handler

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query=query)
    