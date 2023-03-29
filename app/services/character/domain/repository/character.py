from abc import ABC


class CharacterRepositoryInterface(ABC):

    def add(self, characters: list):
        raise NotImplemented()
