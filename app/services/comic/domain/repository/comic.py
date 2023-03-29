from abc import ABC


class ComicRepositoryInterface(ABC):

    def add(self, comics: list):
        raise NotImplemented()

    def get_comic(self, comic_name: str = None, characters: bool = 0):
        raise NotImplemented()
