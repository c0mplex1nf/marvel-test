import requests
import uuid
import os
from app.shared.domain.models.comic import Comic
from app.services.comic.domain.events.comic_created import ComicCreated
from app.shared.domain.queue_interface import QueueClientInterface
from app.services.comic.domain.commands.command_interface import CommandInterface
from app.services.comic.domain.events.comic_event_bus_interface import ComicEventBusInterface
from app.services.comic.domain.repository.comic import ComicRepositoryInterface


class CreateComicHandler():

    def __init__(self, marvel_id: int, villain: str, code: str, command: CommandInterface, repository: ComicRepositoryInterface, event_bus: ComicEventBusInterface, character_queue: QueueClientInterface) -> None:
        self.code = code
        self.marvel_id = marvel_id
        self.villain = villain
        self.apikey = os.environ['AUTH_TOKEN_PUBLIC']
        self.uri = 'https://gateway.marvel.com:443/v1/public/characters'
        self.bus = event_bus
        self.repository = repository
        self.command = command
        self.character_queue = character_queue

    def handler(self):
        uri = uri = self.uri + \
            f'/{self.marvel_id}/comics?apikey={self.apikey}&limit=100&hash=4c60e6392e9fda6fcf400a41b59eb4c3&ts=1680085100'
        comics_data = requests.get(uri).json()
        comics = []
        characters = []

        for comic in comics_data['data']['results']:
            comic_id = str(uuid.uuid4())
            comics.append(Comic(id=comic_id, digital_id=comic['digitalId'], title=comic['title'], description=comic[
                'description'], villain_id=self.villain))

            for character in comic['characters']['items']:
                character_id = str(uuid.uuid4())
                character['id'] = character_id
                character['comic_id'] = comic_id
                characters.append(character)

        self.command.handler(repository=self.repository, comics=comics)

        event = ComicCreated(func_name=self.character_queue.send_message, data={
            'characters': characters})

        self.bus.add_listener(event)
        self.bus.emit(event)
        self.bus.remove_listener(event)
