from config import db, ma


class MysteryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    reserved = db.Column(db.Boolean)

    def __init__(self, title, reserved):
        self.title = title
        self.reserved = reserved


class MysterySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MysteryModel


mystery_schema = MysterySchema()
mysteries_schema = MysterySchema(many=True)




