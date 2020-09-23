import os
from config import db

if os.path.exists("db.sqlite"):
    os.remove("db.sqlite")

db.create_all()






