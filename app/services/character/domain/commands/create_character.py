from app.services.character.domain.repository.character import CharacterRepositoryInterface
from app.services.comic.domain.commands.command_interface import CommandInterface


class CreateCharacter(CommandInterface):

    def handler(self, repository: CharacterRepositoryInterface, characters: list):
        try:
            repository.add(characters=characters)
        except Exception:
            raise
