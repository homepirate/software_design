from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .attachment import Attachment


@dataclass
class Message(Base):
    text: str = ""
    sender: str = ""
    attachments: list['Attachment'] = field(default_factory=list)
    confirmed: bool = False

    def confirm(self, confirming_party: str):
        if self.sender == confirming_party:
            raise ValueError("Подтверждение сообщения доступно только противоположной стороне.")
        self.confirmed = True