from models import Driver
from database import DRIVERS_DICT
dr = Driver(full_name="fdfdf", active=True)

dr.save()

print(DRIVERS_DICT)