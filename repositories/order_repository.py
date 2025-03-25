from models import TransportationOrder
import database

class OrderRepository:

    def save(self, order: TransportationOrder):
        database.ORDERS_ID += 1
        order.id = database.ORDERS_ID
        database.ORDERS_DICT[order.id] = order

    def get_by_id(self, order_id: int) -> TransportationOrder | None:
        return database.ORDERS_DICT.get(order_id)

    def delete(self, order_id: int):
        if order_id in database.ORDERS_DICT:
            del database.ORDERS_DICT[order_id]
        else:
            raise ValueError(f"Заявка с id {order_id} не существует.")
