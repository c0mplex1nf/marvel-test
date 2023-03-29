import requests
import uuid
import os
from datetime import datetime
from app.shared.domain.models.villain import Villain
from app.shared.domain.models.log import Log
from app.services.villain.domain.events.villain_created import VillainCreated
from app.shared.domain.queue_interface import QueueClientInterface
from app.services.villain.domain.commands.command_interface import CommandInterface
from app.services.villain.domain.events.villain_event_bus_interface import VillainEventBusInterface
from app.services.villain.domain.repository.villain import VillainRepositoryInterface


class CreateVillainHandler():

    def __init__(self, code: str, command: CommandInterface, repository: VillainRepositoryInterface, event_bus: VillainEventBusInterface, comic_queue: QueueClientInterface) -> None:
        self.code = code
        self.apikey = os.environ['AUTH_TOKEN_PUBLIC']
        self.uri = 'https://gateway.marvel.com:443/v1/public/characters'
        self.bus = event_bus
        self.repository = repository
        self.command = command
        self.comic_queue = comic_queue

    def handler(self):
        now = datetime.now()
        uri = self.uri + \
            f'?name={self.code}&apikey={self.apikey}&hash=4c60e6392e9fda6fcf400a41b59eb4c3&ts=1680085100'
        log_count = self.repository.log_count(self.code)
        last_log = self.repository.get_last_log()
        seconds_difference = 100000

        if last_log:
            seconds_difference = (now-last_log.created_at).total_seconds()

        if seconds_difference < 30:
            return 'You reach the max amount of requests pleas wait at least 30 seconds for the next import'

        if log_count:
            return 'This Villain was already imported'

        villain_data = requests.get(uri).json()['data']['results'][0]

        if 'message' in villain_data:
            return villain_data['message']

        if not villain_data:
            return 'Probably the Marvel Hero you send does not exist'

        id = str(uuid.uuid4())
        log_id = str(uuid.uuid4())

        villain = Villain(
            id=id, name=villain_data['name'].lower(), description=villain_data['description'], image=villain_data['thumbnail']['path'])

        log = Log(id=log_id, villain_name=self.code)

        self.command.handler(
            villain=villain, repository=self.repository, log=log)

        event = VillainCreated(func_name=self.comic_queue.send_message, data={
            'uuid': id, 'villain': villain_data['id'], 'name': self.code})

        self.bus.add_listener(event)
        self.bus.emit(event)
        self.bus.remove_listener(event)
