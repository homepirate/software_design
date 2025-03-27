from dataclasses import dataclass

import database
from .base import Base


@dataclass
class Attachment(Base):
    filename: str = ""
    content: bytes = b""

    def __post_init__(self):
        database.ATTACHMENT_ID += 1
        self.id = database.ATTACHMENT_ID