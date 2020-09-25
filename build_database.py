import os
import secrets
from config import db
from models import PrayerModel, MysteryModel

if os.path.exists("db.sqlite"):
    os.remove("db.sqlite")

prayer = PrayerModel(endpoint=str(secrets.token_hex(5)))
mystery = MysteryModel(prayer_id=prayer.id)
print(prayer.endpoint)

db.create_all()






