from dataclasses import dataclass
from app.services.comic.domain.events.event_interface import EventInterface


@dataclass(unsafe_hash=True)
class ComicCreated(EventInterface):
    name: str = 'comic-created'
