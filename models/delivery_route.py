from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryRoute:
    origin: str
    destination: str