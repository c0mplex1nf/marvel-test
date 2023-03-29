from dataclasses import dataclass, field
from typing import List
from app.shared.domain.models.comic import Comic


@dataclass(unsafe_hash=True)
class Villain:
    id: str
    name: str
    description: str
    image: str
    comics: List[Comic] = field(default_factory=list)
