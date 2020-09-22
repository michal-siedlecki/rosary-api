from config import db, ma


class MysteryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    reserved = db.Column(db.Boolean, default=False)
    prayer_id = db.Column(db.Integer, db.ForeignKey('prayers.id'), nullable=False)

    def __init__(self, title, prayer_id):
        self.title = title
        self.prayer_id = prayer_id



class MysterySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MysteryModel


class PrayerModel(db.Model):
    __tablename__ = "prayers"
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(10))
    mysteries = db.relationship('MysteryModel', backref='prayer', lazy=True)

class PrayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PrayerModel

mystery_schema = MysterySchema()
mysteries_schema = MysterySchema(many=True)
prayer_schema = PrayerSchema()




