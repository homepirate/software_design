from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from .base import Base
from .delivery_route import DeliveryRoute
from .order_status import OrderStatus

if TYPE_CHECKING:
    from .message import Message

@dataclass
class TransportationOrder(Base):
    status: OrderStatus = field(default_factory=OrderStatus.active)
    delivery_route: DeliveryRoute | None= None
    messages: list['Message'] = field(default_factory=list)
    last_activity: datetime = field(default_factory=datetime.now)

    def add_message(self, message: Message):

        if self.status.status != OrderStatus.ACTIVE:
            raise ValueError("Сообщения могут добавляться только к активной заявке.")
        self.messages.append(message)
        self.last_activity = datetime.now()

    def close_order(self):
        self.status = OrderStatus.closed()

    def check_inactivity(self, inactivity_threshold: timedelta):
        if datetime.now() - self.last_activity > inactivity_threshold:
            self.close_order()