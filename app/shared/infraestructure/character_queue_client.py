import pika
import os
import json
import uuid
from aio_pika import logger, connect_robust
from app.shared.domain.queue_interface import QueueClientInterface
from app.services.character.domain.commands.create_character import CreateCharacter
from app.services.character.infraestructure.repository.character import CharacterSqlAlchemyRepository
from app.services.character.application.command_handlers.create_character_handler import CreateCharacterHandler
from config.database import get_session


class CharacterQueueClient(QueueClientInterface):

    def __init__(self):
        self.queue_name = os.environ.get('CHARACTER_QUEUE', 'character-queue')
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
        data = json.loads(body)
        logger.info('Received message')
        if body:
            session = get_session()
            character_handler = CreateCharacterHandler(characters=data['characters'], command=CreateCharacter(),
                                                       repository=CharacterSqlAlchemyRepository(session=session))
            character_handler.handler()

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
