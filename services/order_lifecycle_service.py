from datetime import datetime, timedelta

from models import TransportationOrder, OrderStatus


class OrderLifecycleService:
    def update_status(self, order: TransportationOrder, new_status: OrderStatus):
        """
        Обновляет статус заявки и фиксирует время активности.
        """
        order.status = new_status
        order.last_activity = datetime.now()

    def auto_close_order_if_inactive(self, order: TransportationOrder, inactivity_threshold: timedelta):
        """
        Проверяет, не нарушен ли порог бездействия, и закрывает заявку, если это необходимо.
        """
        order.check_inactivity(inactivity_threshold)