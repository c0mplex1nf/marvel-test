from app.services.villain.domain.repository.villain import VillainRepositoryInterface
from app.services.villain.domain.commands.command_interface import CommandInterface
from app.shared.domain.models.villain import Villain
from app.shared.domain.models.log import Log


class CreateVillain(CommandInterface):

    def handler(self, repository: VillainRepositoryInterface, villain: Villain, log: Log):
        try:
            repository.add(villain)
            repository.add_log(log=log)
        except Exception:
            raise
