import uuid
from app.shared.domain.models.character import Character
from app.services.character.domain.commands.command_interface import CommandInterface
from app.services.character.domain.repository.character import CharacterRepositoryInterface


class CreateCharacterHandler():

    def __init__(self, characters: list, command: CommandInterface, repository: CharacterRepositoryInterface) -> None:
        self.repository = repository
        self.command = command
        self.characters = characters

    def handler(self):
        characters_arr = []

        for character in self.characters:
            id = str(uuid.uuid4())
            characters_arr.append(
                Character(id=id, name=character['name'], uri=character['resourceURI'], comic_id=character['comic_id']))

        self.command.handler(repository=self.repository,
                             characters=characters_arr)
