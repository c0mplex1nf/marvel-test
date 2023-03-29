from fastapi import Depends
from sqlalchemy import insert
from app.services.villain.domain.repository.villain import VillainRepositoryInterface
from app.shared.domain.models.villain import Villain
from app.shared.domain.models.character import Character
from app.shared.domain.models.comic import Comic
from app.shared.domain.models.log import Log
from config.database import get_session


class VillainSqlAlchemyRepository(VillainRepositoryInterface):

    def __init__(self, session=Depends(get_session)):
        self.session = session

    def add(self, villain: Villain):
        self.session.add(villain)
        self.session.commit()

    def add_log(self, log: Log):
        self.session.add(log)
        self.session.commit()

    def log_count(self, code: str):
        r = self.session.query(Log).filter_by(villain_name=code).count()
        return r

    def get_last_log(self):
        r = self.session.query(Log).order_by(Log.created_at.desc()).first()
        return r

    def get_villain_characters(self, villain_code='spectrum', filter_name=None):

        r = self.session.query(Villain).join(Villain.comics).join(
            Comic.characters).filter(Villain.name == villain_code)

        if filter_name:
            r = self.session.query(Character).join(Villain.comics).join(Comic.characters).filter(
                Villain.name == villain_code, Comic.title == filter_name)

        return r.all()
