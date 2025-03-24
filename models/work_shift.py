from dataclasses import dataclass
from .base import Base
from datetime import datetime


@dataclass
class WorkShift(Base):
    start: datetime = datetime.now()
    end: datetime = datetime.now()

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("Время окончания смены должно быть позже времени начала.")