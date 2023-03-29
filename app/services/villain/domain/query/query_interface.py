from abc import ABC
from app.services.villain.domain.repository.villain import VillainRepositoryInterface


class QueryInterface(ABC):

    def handler(self, repository: VillainRepositoryInterface, filter_villain: str = None, villain_code: str = 'spectrum'):
        raise NotImplemented()
