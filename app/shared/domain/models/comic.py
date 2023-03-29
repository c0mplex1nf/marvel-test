from dataclasses import dataclass, field
from app.shared.domain.models.character import Character
from typing import List


@dataclass(unsafe_hash=True)
class Comic:
    id: str
    digital_id: str
    title: str
    description: str
    villain_id: str
    characters: List[Character] = field(default_factory=list)
