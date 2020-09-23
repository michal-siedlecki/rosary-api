import json
import secrets
from flask import request

from models import MysteryModel, mystery_schema, mysteries_schema, PrayerModel
from config import app, db


@app.route('/api/1/<endpoint>', methods=['GET'])
def get_prayer(endpoint):
    prayer = PrayerModel.query.filter_by(endpoint=endpoint).first()
    result = MysteryModel.query.filter_by(prayer_id=prayer.id)
    return mysteries_schema.jsonify(result)


@app.route('/api/1', methods=['POST'])
def create_prayer():
    parts = request.get_json(force=True).get('parts')
    with open('rosary.json', 'r') as f:
        rosary = json.load(f)

    endp = str(secrets.token_hex(5))
    prayer = PrayerModel(endpoint=endp)
    db.session.add(prayer)
    db.session.commit()

    for part in parts:
        for m in rosary.get(part):
            mystery = MysteryModel(title=m, prayer_id=prayer.id)
            prayer.mysteries.append(mystery)
            db.session.add(prayer)
            db.session.commit()

    return get_prayer(endpoint=endp)


@app.route('/api/1/<mystery_id>', methods=['PUT'])
def update_mystery(mystery_id):
    mystery = MysteryModel.query.get(mystery_id)
    data = request.get_json(force=True)
    reserved = data.get('reserved')
    mystery.reserved = reserved if reserved else mystery.reserved
    db.session.commit()
    return mystery_schema.jsonify(mystery)


if __name__ == '__main__':
    app.run(debug=True)
