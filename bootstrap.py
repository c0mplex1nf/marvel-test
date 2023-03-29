import asyncio
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from config import database
from app.services.villain.presentation.controllers.villain import VillainController
from app.shared.infraestructure.comic_queue_client import ComicQueueClient
from app.shared.infraestructure.character_queue_client import CharacterQueueClient


class Bootstrap(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_dotenv()
        self.metadata = database.start_mappers()
        self.villain = VillainController()
        self.comic_queue_client = ComicQueueClient()
        self.character_queue_client = CharacterQueueClient()


app = Bootstrap()
app.include_router(app.villain.router, prefix="/villain")


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task_comic = loop.create_task(app.comic_queue_client.consume(loop=loop))
    task_character = loop.create_task(
        app.character_queue_client.consume(loop=loop))
    await task_comic
    await task_character
