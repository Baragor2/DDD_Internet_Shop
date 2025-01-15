from pydantic import BaseModel

from infra.repositories.filters.base import GetFilters as GetInfraFilters

class GetFilters(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetInfraFilters(
            limit=self.limit,
            offset=self.offset,
        )
    