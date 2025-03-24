from datetime import datetime

from errors import ShiftOverlapError
from models import WorkShift, Driver
from database import DRIVERS_DICT

def get_driver_by_id(id: int):
    return DRIVERS_DICT.get(id, None)

def add_work_shift(id: int, shift: WorkShift):
    driver: Driver| None = get_driver_by_id(id)
    if not driver:
        raise ValueError("Водитель отсутствует")

    for existing_shift in driver.schedule:
        if not (shift.end <= existing_shift.start or shift.start >= existing_shift.end):
            raise ShiftOverlapError("Новая смена пересекается с уже существующей.")
    driver.schedule.append(shift)

def remove_work_shift(id: int, shift_id: int):
    driver: Driver| None = get_driver_by_id(id)
    if not driver:
        raise ValueError("Водитель отсутствует")

    for shift in driver.schedule:
        if shift.id == shift_id:
            driver.schedule.remove(shift)
            return
    raise ValueError("Смена с таким id не найдена в расписании водителя.")

def get_work_shift_by_date(id: int, date_str: str) -> list[WorkShift]:
    driver: Driver| None = get_driver_by_id(id)
    if not driver:
        raise ValueError("Водитель отсутствует")

    search_date = datetime.strptime(date_str, "%d.%m.%Y").date()

    shifts_on_date = [
        shift for shift in driver.schedule
        if shift.start.date() <= search_date <= shift.end.date()
    ]
    return shifts_on_date


def is_driver_available_at(id: int, moment: datetime) -> bool:
    driver: Driver | None = get_driver_by_id(id)
    if not driver:
        raise ValueError("Водитель отсутствует")
    if not driver.active:
        return False
    for shift in driver.schedule:
        if shift.start <= moment <= shift.end:
            return False
    return True