from abc import ABC
from app.services.villain.domain.repository.villain import VillainRepositoryInterface
from app.shared.domain.models.villain import Villain
from app.shared.domain.models.log import Log


class CommandInterface(ABC):

    def handler(self, repository: VillainRepositoryInterface, villain: Villain, log: Log):
        raise NotImplemented()
