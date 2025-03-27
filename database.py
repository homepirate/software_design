from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Driver, TransportationOrder

DRIVERS_ID = 0
ORDERS_ID = 0
MESSAGE_ID = 0
ATTACHMENT_ID = 0
WORKSHIFT_ID = 0

DRIVERS_DICT: dict[int, "Driver"] = dict()
ORDERS_DICT: dict[int, "TransportationOrder"] = dict()
