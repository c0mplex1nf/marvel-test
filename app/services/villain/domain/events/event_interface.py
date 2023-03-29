from dataclasses import dataclass, field
from typing import Callable
from abc import ABC


@dataclass(unsafe_hash=True)
class EventInterface(ABC):
    func_name: Callable
    data: str
    name: str
