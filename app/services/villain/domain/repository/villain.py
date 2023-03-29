from abc import ABC
from app.shared.domain.models.villain import Villain
from app.shared.domain.models.log import Log


class VillainRepositoryInterface(ABC):

    def add(self, villain: Villain) -> None:
        raise NotImplemented()

    def add_log(self, log: Log) -> None:
        raise NotImplemented()

    def log_count(self, code: str) -> int:
        raise NotImplemented()

    def get_last_log(self):
        raise NotImplemented()

    def get_villain_characters(self, villain_code, filter_name):
        raise NotImplemented()
