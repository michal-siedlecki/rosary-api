import os
import secrets
from config import db
from models import MysteryModel, PrayerModel

# Data to initialize database with
ROSARY = {
    "radosne" : [
        "Zwiastowanie Najswietszej Marii Pannie",
        "Nawiedzenie Swietej Elzbiety",
        "Narodzenie Jezusa Chrystusa",
        "Ofiarowanie Jezusa w Swiatyni",
        "Odnalezienie Jezusa w Swiatyni"
    ],
    "bolesne": [
        "Modlitwa w Ogrojcu",
        "Biczowanie Pana Jezusa",
        "Cierniem Ukoronowanie Pana Jezusa",
        "Droga Krzyzowa",
        "Smierc na Krzyzu"
    ],
    "chwalebne": [
        "Zmartwychwstanie Pana Jezusa",
        "Wniebowstapienie Pana Jezusa",
        "Zeslanie Ducha Swietego na Maryje i apostolow",
        "Wniebowziecie Najswietszej Marii Panny",
        "Ukoronowanie Najswietszej Marii Panny"
    ],
    "swatla": [
        "Chrzest Pana Jezusa",
        "Wesele w Kanie Galilejskiej",
        "Gloszenie Krolewstwa Bozego i wzywanie do nawrocenia",
        "Przemienienie na gorze Tabor",
        "Ustanowienie Eucharystii"
    ]
}


# Delete database file if it exists currently
if os.path.exists("db.sqlite"):
    os.remove("db.sqlite")

db.create_all()

endp = str(secrets.token_hex(5))
prayer = PrayerModel(endpoint=endp)
db.session.add(prayer)
db.session.commit()
mysteries = []
mysteries.append(ROSARY.get('radosne'))
mysteries.append(ROSARY.get('bolesne'))
mysteries.append(ROSARY.get('chwalebne'))
print(endp)

for part in mysteries:
    for m in part:
        mystery = MysteryModel(title=m, prayer_id=prayer.id)
        prayer.mysteries.append(mystery)
        db.session.add(prayer)
        db.session.commit()


