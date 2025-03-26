from dataclasses import dataclass, field
from datetime import datetime, timedelta

from errors import OrderOperationError
from .base import Base
from .delivery_route import DeliveryRoute
from .order_status import OrderStatus
from .message import Message

@dataclass
class TransportationOrder(Base):
    status: OrderStatus = field(default_factory=OrderStatus.active)
    delivery_route: DeliveryRoute | None= None
    messages: list[Message] = field(default_factory=list)
    last_activity: datetime = field(default_factory=datetime.now)

    def add_message(self, message: Message):
        if self.status.status != OrderStatus.ACTIVE:
            raise OrderOperationError("Сообщения могут добавляться только к активной заявке.")
        self.messages.append(message)
        self.last_activity = datetime.now()

    def change_route(self, new_route: DeliveryRoute) -> None:
        if self.status.status != OrderStatus.ACTIVE:
            raise OrderOperationError("Нельзя изменить маршрут закрытой заявки.")
        self.delivery_route = new_route
        self.last_activity = datetime.now()

    def close_order(self):
        if self.status.status == OrderStatus.CLOSED:
            raise OrderOperationError("Заявка уже закрыта.")
        self.status = OrderStatus.closed()

    def check_inactivity(self, inactivity_threshold: timedelta):
        if datetime.now() - self.last_activity > inactivity_threshold:
            self.close_order()