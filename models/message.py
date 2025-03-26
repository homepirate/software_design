from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from errors import EmptyMessageError
from .base import Base

if TYPE_CHECKING:
    from .attachment import Attachment


@dataclass
class Message(Base):
    text: str = ""
    sender: str = ""
    attachments: list['Attachment'] = field(default_factory=list)
    confirmed: bool = False

    def __post_init__(self):
        if not self.text.strip():
            raise EmptyMessageError("Сообщение не может быть пустым.")
        if not self.sender.strip():
            raise EmptyMessageError("Отправитель не может быть пустым.")

    def confirm(self, confirming_party: str):
        if self.sender == confirming_party:
            raise ValueError("Подтверждение сообщения доступно только противоположной стороне.")
        self.confirmed = True