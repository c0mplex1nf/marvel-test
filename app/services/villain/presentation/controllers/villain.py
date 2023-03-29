import json
from fastapi import APIRouter, Depends, Request
from app.services.villain.presentation.controllers.controller import Controller
from app.services.villain.application.command_handlers.create_villain_handler import CreateVillainHandler
from app.services.villain.application.query_handlers.get_villain_characters_handler import QueryVillianComicCharacterHandler
from app.services.villain.domain.commands.create_villain import CreateVillain
from app.services.villain.domain.query.query_characters import QueryCharactersByVillan
from app.services.villain.infraestructure.repository.villain import VillainSqlAlchemyRepository
from app.shared.infraestructure.event_bus import EventBus
from app.shared.infraestructure.comic_queue_client import ComicQueueClient


class VillainController(Controller):

    router = APIRouter()

    def __init__(self) -> None:
        super().__init__()

    @router.get('/import/{code}')
    async def import_villains(code: str = 'spectrum', command=Depends(CreateVillain), repository=Depends(VillainSqlAlchemyRepository),
                              event_bus=Depends(EventBus), comic_queue=Depends(ComicQueueClient)) -> json:

        response = {'message': 'The villain have been saved'}

        handler = CreateVillainHandler(
            code=code, command=command, repository=repository, event_bus=event_bus, comic_queue=comic_queue)

        errors = handler.handler()

        if errors:
            response['message'] = errors

        return response

    @router.get('/{code}')
    async def list_players(code: str = 'spectrum', comic_name: str = None, repository=Depends(VillainSqlAlchemyRepository), query=Depends(QueryCharactersByVillan)):
        response = {}
        query_handler = QueryVillianComicCharacterHandler(
            repository=repository, query=query, villain_code=code, filter_villain=comic_name)
        query_response = query_handler.handler()
        response['body'] = query_response
        return response
