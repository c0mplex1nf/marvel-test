from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Character:
    id: str
    name: str
    uri: str
    comic_id: str
