from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

from errors import ValidationError
from .base import Base
import database

if TYPE_CHECKING:
    from .work_shift import WorkShift

@dataclass
class Driver(Base):
    full_name: str = ""
    active: bool = True
    schedule: list["WorkShift"] = field(default_factory=list)

    def __post_init__(self):
        name = self.full_name.strip()
        if not name:
            raise ValidationError("Полное имя не может быть пустым.")
        if any(char.isdigit() for char in name):
            raise ValidationError("Полное имя не должно содержать цифр.")
        if len(name.split()) < 2:
            raise ValidationError("Укажите как минимум имя и фамилию.")

        database.DRIVERS_ID += 1
        self.id = database.DRIVERS_ID

    def save(self):
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

    def is_driver_available_at(self, moment: datetime) -> bool:
        if not self.active:
            return False
        for shift in self.schedule:
            if shift.start <= moment <= shift.end:
                return False
        return True