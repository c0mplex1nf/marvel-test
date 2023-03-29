import pika
import os
import json
import uuid
import ast
from aio_pika import logger, connect_robust
from app.shared.domain.queue_interface import QueueClientInterface
from app.services.comic.domain.commands.create_comic import CreateComic
from app.shared.infraestructure.event_bus import EventBus
from app.services.comic.infraestructure.repository.comic import ComicSqlAlchemyRepository
from app.services.comic.application.command_handlers.create_comic_handler import CreateComicHandler
from app.shared.infraestructure.character_queue_client import CharacterQueueClient
from config.database import get_session


class ComicQueueClient(QueueClientInterface):

    def __init__(self):
        self.queue_name = os.environ.get('COMIC_QUEUE', 'comic-queue')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ.get(
                'RABBIT_HOST', 'rabbitmq'), heartbeat=0)
        )
        self.channel = self.connection.channel()
        self.queue = self.channel.queue_declare(queue=self.queue_name)
        self.callback_queue = self.queue.method.queue
        self.response = None
        logger.info('connection initialized')

    async def consume(self, loop):
        connection = await connect_robust(host=os.environ.get('RABBIT_HOST', 'rabbitmq'), port=5672, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(self.queue_name)
        await queue.consume(self.process_incoming_message, no_ack=False)
        logger.info('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        await message.ack()
        body = message.body.decode("UTF-8")
        data = ast.literal_eval(body)
        logger.info('Received message')
        if data:
            session = get_session()
            comic_handler = CreateComicHandler(villain=data['uuid'], marvel_id=data['villain'], code=data['name'], command=CreateComic(),
                                               repository=ComicSqlAlchemyRepository(session=session), event_bus=EventBus(),
                                               character_queue=CharacterQueueClient())

            comic_handler.handler()

    async def send_message(self, message: dict):

        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
