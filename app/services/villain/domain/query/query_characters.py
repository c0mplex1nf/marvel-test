from app.services.villain.domain.repository.villain import VillainRepositoryInterface
from app.services.villain.domain.commands.command_interface import CommandInterface


class QueryCharactersByVillan(CommandInterface):

    def handler(self, repository: VillainRepositoryInterface, filter_villain: str = None, villain_code: str = 'spectrum'):
        try:
            r = repository.get_villain_characters(
                villain_code=villain_code, filter_name=filter_villain)
            return r
        except Exception:
            raise
