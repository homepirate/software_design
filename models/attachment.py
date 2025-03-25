from dataclasses import dataclass

from .base import Base


@dataclass
class Attachment(Base):
    filename: str = ""
    content: bytes = b""