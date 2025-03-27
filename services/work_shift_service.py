from datetime import datetime, timedelta

from errors import ShiftOverlapError, ObjectNotFoundError
from models import WorkShift, Driver
from database import DRIVERS_DICT


MAX_SHIFT_HOURS = 12

def get_driver_by_id(id: int) -> Driver:
    driver = DRIVERS_DICT.get(id, None)
    if not driver:
        raise ObjectNotFoundError("Водитель отсутствует")
    return driver



def add_work_shift(id: int, shift: WorkShift):
    driver = get_driver_by_id(id)

    if not driver.active:
        raise ValueError("Водитель не активен")

    if (shift.end - shift.start) > timedelta(hours=MAX_SHIFT_HOURS):
        raise ValueError(f"Длительность смены не должна превышать {MAX_SHIFT_HOURS} часов.")

    for existing_shift in driver.schedule:
        if not (shift.end <= existing_shift.start or shift.start >= existing_shift.end):
            raise ShiftOverlapError("Новая смена пересекается с уже существующей.")
    driver.schedule.append(shift)

def remove_work_shift(id: int, shift_id: int):
    driver = get_driver_by_id(id)

    for shift in driver.schedule:
        if shift.id == shift_id:
            driver.schedule.remove(shift)
            return
    raise ObjectNotFoundError(f"Смена с {id=} не найдена в расписании водителя.")

def get_work_shift_by_date(id: int, date_str: str) -> list[WorkShift]:
    driver = get_driver_by_id(id)

    search_date = datetime.strptime(date_str, "%d.%m.%Y").date()

    shifts_on_date = [
        shift for shift in driver.schedule
        if shift.start.date() <= search_date <= shift.end.date()
    ]
    return shifts_on_date
