from dataclasses import dataclass
from app.services.villain.domain.events.event_interface import EventInterface


@dataclass(unsafe_hash=True)
class VillainCreated(EventInterface):
    name: str = 'villain-created'
