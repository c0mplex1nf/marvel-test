from dataclasses import dataclass, field
from datetime import datetime


@dataclass(unsafe_hash=True)
class Log:
    id: str
    villain_name: str
    created_at: datetime = field(default_factory=datetime.now)
