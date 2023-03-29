from app.services.comic.domain.repository.comic import ComicRepositoryInterface
from app.services.comic.domain.commands.command_interface import CommandInterface


class CreateComic(CommandInterface):

    def handler(self, repository: ComicRepositoryInterface, comics: list):
        try:
            repository.add(comics=comics)
        except Exception:
            raise
