from datetime import datetime, timedelta

from models import Driver, WorkShift, Message, DeliveryRoute, TransportationOrder, OrderStatus
from services.work_shift_service import add_work_shift, remove_work_shift, get_work_shift_by_date
from services.fraud_detection_service import FraudDetectionService
from services.order_lifecycle_service import OrderLifecycleService
from errors import ShiftOverlapError, EmptyMessageError, OrderOperationError


def main():
    print("=== Валидация Driver ===")
    try:
        Driver(full_name="123")
    except ValueError as err:
        print("Ошибка создания водителя:", err)

    driver = Driver(full_name="Иван Иванов")
    driver.save()
    print("Создан водитель:", driver)

    print("\n=== Добавление смен ===")
    try:
        WorkShift(start=datetime(2025,3,27,18), end=datetime(2025,3,27,9))
    except ValueError as err:
        print("Ошибка создания смены:", err)

    shift1 = WorkShift(start=datetime(2025,3,27,9), end=datetime(2025,3,27,17))
    add_work_shift(driver.id, shift1)  # citeturn3file1
    print("Добавлена смена:", shift1)

    try:
        overlapping = WorkShift(start=datetime(2025,3,27,16), end=datetime(2025,3,27,20))
        add_work_shift(driver.id, overlapping)
    except ShiftOverlapError as err:
        print("Ошибка пересечения смен:", err)

    try:
        long_shift = WorkShift(start=datetime(2025,3,27,9), end=datetime(2025,3,28,9))
        add_work_shift(driver.id, long_shift)
    except ValueError as err:
        print("Ошибка длительности смены:", err)

    print("Смены на 27.03.2025:", get_work_shift_by_date(driver.id, "27.03.2025"))
    remove_work_shift(driver.id, shift1.id)
    print("Смена удалена")

    print("\n=== Сообщения ===")
    try:
        Message(text="  ", sender="User")
    except EmptyMessageError as err:
        print("Ошибка сообщения:", err)

    msg = Message(text="Привет", sender="User")
    print("Создано сообщение:", msg)
    try:
        msg.confirm("User")
    except ValueError as err:
        print("Ошибка подтверждения сообщения:", err)
    msg.confirm("Admin")
    print("Сообщение подтверждено:", msg.confirmed)

    print("\n=== Заказ ===")
    order = TransportationOrder()
    order.add_message(msg)
    route = DeliveryRoute(origin="Город A", destination="Город B")
    order.change_route(route)
    print("Заказ создан и обновлен:", order)

    order.close_order()
    try:
        order.add_message(msg)
    except OrderOperationError as err:
        print("Ошибка добавления сообщения к закрытому заказу:", err)

    fraud_service = FraudDetectionService()
    print("Подозрительный заказ?", fraud_service.check_order(order))

    lifecycle = OrderLifecycleService()
    lifecycle.add_order_to_db(order)
    lifecycle.update_status(order.id, OrderStatus.cancelled())
    print("Статус заказа после отмены:", order.status)

    order.last_activity = datetime.now() - timedelta(days=1)
    lifecycle.auto_close_order_if_inactive(order.id, timedelta(hours=12))
    print("Статус после проверки неактивности:", order.status)


if __name__ == '__main__':
    main()
