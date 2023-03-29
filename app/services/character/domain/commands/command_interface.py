from abc import ABC
from app.services.character.domain.repository.character import CharacterRepositoryInterface


class CommandInterface(ABC):

    def handler(self, repository: CharacterRepositoryInterface, characters: list):
        raise NotImplemented()
