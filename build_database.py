import os
from config import db
from models import MysteryModel

# Data to initialize database with
MYSTERIES = [
    {"title": "Zwiastowanie Najswietszej Marii Pannie"},
    {"title": "Nawiedzenie Swietej Elzbiety"},
    {"title": "Narodzenie Jezusa Chrystusa"},
    {"title": "Ofiarowanie Jezusa w Swiatyni"},
    {"title": "Odnalezienie Jezusa w Swiatyni"}
]

# Delete database file if it exists currently
if os.path.exists("db.sqlite"):
    os.remove("db.sqlite")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for mystery in MYSTERIES:
    m = MysteryModel(title=mystery.get("title"), reserved=False)
    db.session.add(m)

db.session.commit()
