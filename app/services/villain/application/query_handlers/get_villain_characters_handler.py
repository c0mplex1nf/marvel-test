from app.services.villain.domain.repository.villain import VillainRepositoryInterface
from app.services.villain.domain.query.query_interface import QueryInterface


class QueryVillianComicCharacterHandler():

    def __init__(self, repository: VillainRepositoryInterface, query: QueryInterface, filter_villain: str = None, villain_code: str = 'spectrum') -> None:
        self.villain_code = villain_code
        self.repository = repository
        self.filter_villain = filter_villain
        self.query = query

    def handler(self):
        r = self.query.handler(repository=self.repository,
                               filter_villain=self.filter_villain, villain_code=self.villain_code)

        return r
