from fastapi import Depends
from app.services.character.domain.repository.character import CharacterRepositoryInterface
from config.database import get_session


class CharacterSqlAlchemyRepository(CharacterRepositoryInterface):

    def __init__(self, session=Depends(get_session)):
        self.session = session

    def add(self, characters: list):
        self.session.bulk_save_objects(characters)
        self.session.commit()
