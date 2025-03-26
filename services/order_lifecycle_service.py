from datetime import datetime, timedelta

from errors import ObjectNotFoundError
from models import TransportationOrder, OrderStatus
from repositories import OrderRepository

class OrderLifecycleService:

    order_repository = OrderRepository()

    def get_order_by_id(self, id: int) -> TransportationOrder:
        transaction_order = self.order_repository.get_by_id(id)

        if not transaction_order:
            raise ObjectNotFoundError(f"Объект с {id=} не найден")
        return transaction_order

    def add_order_to_db(self, order: TransportationOrder):
        self.order_repository.save(order)

    def update_status(self, order_id: int, new_status: OrderStatus):
        order = self.get_order_by_id(order_id)
        order.status = new_status
        order.last_activity = datetime.now()

    def auto_close_order_if_inactive(self, order_id: int, inactivity_threshold: timedelta):
        order = self.get_order_by_id(order_id)
        order.check_inactivity(inactivity_threshold)