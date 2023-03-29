from abc import ABC
from app.services.comic.domain.repository.comic import ComicRepositoryInterface


class CommandInterface(ABC):

    def handler(self, repository: ComicRepositoryInterface, comics: list):
        raise NotImplemented()
