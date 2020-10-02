import datetime
from config import db, ma


class MysteryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    reserved = db.Column(db.Boolean, default=False)
    prayer_id = db.Column(db.Integer, db.ForeignKey('prayers.id'), nullable=False)
    prayer_endpoint = db.Column(db.String(30))


class MysterySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MysteryModel
        fields = ['id', 'title', 'reserved', 'prayer_id']


class PrayerModel(db.Model):
    __tablename__ = "prayers"
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(30))
    mysteries = db.relationship('MysteryModel', backref='prayer', lazy=True)
    duration_days = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def delete_expired(cls, timestamp, duration_days):

        limit = datetime.datetime.utcnow() - datetime.timedelta(days=duration_days)
        cls.query.filter(timestamp < limit).delete()
        db.session.commit()


mystery_schema = MysterySchema()
mysteries_schema = MysterySchema(many=True)
