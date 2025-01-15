from dataclasses import dataclass


@dataclass
class GetFilters:
    limit: int = 10
    offset: int = 0

