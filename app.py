import json
import secrets
from flask import request, redirect, abort

from models import MysteryModel, mystery_schema, mysteries_schema, PrayerModel
from config import app, db


@app.route('/api/1/<endpoint>', methods=['GET'])
def get_prayer(endpoint):

    prayer = PrayerModel.query.filter_by(endpoint=endpoint).first()
    if not prayer:
        abort(404, description="Resource not found")
    result = MysteryModel.query.filter_by(prayer_id=prayer.id)

    PrayerModel.delete_expired(timestamp=prayer.timestamp, duration_days=prayer.duration_days)

    return mysteries_schema.jsonify(result)


@app.route('/api/1', methods=['POST'])
def create_prayer():
    parts = request.get_json(force=True).get('parts')
    duration = request.get_json(force=True).get('duration')

    with open('rosary.json', 'r') as f:
        rosary = json.load(f)

    endpoint = str(secrets.token_hex(5))
    prayer = PrayerModel(endpoint=endpoint, duration_days=duration)
    db.session.add(prayer)
    db.session.commit()

    for part in parts:
        for m in rosary.get(part):
            mystery = MysteryModel(title=m, prayer_id=prayer.id)
            prayer.mysteries.append(mystery)
            db.session.add(prayer)
            db.session.commit()

    return redirect(request.url + '/' + endpoint, code=302)


@app.route('/api/1/<prayer_endp>/<mystery_id>', methods=['PUT'])
def update_mystery(prayer_endp, mystery_id):
    prayer = PrayerModel.query.filter_by(endpoint=prayer_endp).first()
    if not prayer:
        abort(404, description="Resource not found")
    mystery = MysteryModel.query.get(mystery_id)
    if mystery not in prayer.mysteries:
        abort(404, description="Resource not found")
    data = request.get_json(force=True)
    reserved = data.get('reserved')
    mystery.reserved = reserved if reserved else mystery.reserved
    db.session.commit()
    return mystery_schema.jsonify(mystery)


if __name__ == '__main__':
    app.run(debug=True)
