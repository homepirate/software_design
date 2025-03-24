from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from .base import Base
import database

if TYPE_CHECKING:
    from .work_shift import WorkShift

@dataclass
class Driver(Base):
    full_name: str = ""
    active: bool = True
    schedule: list["WorkShift"] = field(default_factory=list)

    def save(self):
        database.DRIVERS_ID += 1
        self.id = database.DRIVERS_ID
        database.DRIVERS_DICT[self.id] = self

    def delete(self):
        if self.id in database.DRIVERS_DICT:
            del database.DRIVERS_DICT[self.id]
        else:
            raise ValueError(f"Водитель с id {self.id} не найден.")

    def update(self, full_name: str = None, active: bool = None):
        if full_name is not None:
            self.full_name = full_name
        if active is not None:
            self.active = active
        self.save()