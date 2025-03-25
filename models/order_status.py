from dataclasses import dataclass


@dataclass(frozen=True)
class OrderStatus:
    status: str

    ACTIVE: str = "Active"
    CLOSED: str = "Closed"
    CANCELLED: str = "Cancelled"

    @classmethod
    def active(cls) -> 'OrderStatus':
        return cls(status=cls.ACTIVE)

    @classmethod
    def closed(cls) -> 'OrderStatus':
        return cls(status=cls.CLOSED)

    @classmethod
    def cancelled(cls) -> 'OrderStatus':
        return cls(status=cls.CANCELLED)