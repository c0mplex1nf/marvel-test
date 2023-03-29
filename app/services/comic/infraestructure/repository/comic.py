from fastapi import Depends
from sqlalchemy import insert
from app.services.comic.domain.repository.comic import ComicRepositoryInterface
from app.shared.domain.models.character import Character
from app.shared.domain.models.comic import Comic
from config.database import get_session


class ComicSqlAlchemyRepository(ComicRepositoryInterface):

    def __init__(self, session=Depends(get_session)):
        self.session = session

    def add(self, comics: list):
        self.session.bulk_save_objects(comics)
        self.session.commit()

    def get_comic(self, comic_title: str = None, characters: bool = 0):
        r = self.session.query(Comic)

        if not characters:
            r = self.session.query(
                Comic.id, Comic.title)

        r = r.filter(Comic.title == comic_title)

        return r.all()
