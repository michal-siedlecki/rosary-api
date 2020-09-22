from flask import request

from models import MysteryModel, mystery_schema, mysteries_schema, PrayerModel, prayer_schema
from config import app, db


@app.route('/api/1', methods=['POST'])
def add_mystery():
    data = request.get_json(force=True)
    title = data.get('title')
    reserved = data.get('reserved')
    new_mystery = MysteryModel(title, reserved)
    db.session.add(new_mystery)
    db.session.commit()
    return mystery_schema.jsonify(request.get_json)

@app.route('/api/1/<endpoint>', methods=['GET'])
def get_prayer(endpoint):
    prayer = PrayerModel.query.filter_by(endpoint=endpoint).first()
    result = MysteryModel.query.filter_by(prayer_id=prayer.id)
    return mysteries_schema.jsonify(result)

@app.route('/api/1', methods=['GET'])
def get_mysteries_list():
    all_mysteries = MysteryModel.query.all()
    result = mysteries_schema.dump(all_mysteries)
    return mysteries_schema.jsonify(result)


@app.route('/api/1/<mystery_id>', methods=['GET'])
def get_mystery(mystery_id):
    mystery = MysteryModel.query.get(mystery_id)
    return mystery_schema.jsonify(mystery)


@app.route('/api/1/<mystery_id>', methods=['PUT'])
def update_mystery(mystery_id):
    mystery = MysteryModel.query.get(mystery_id)
    data = request.get_json(force=True)
    title = data.get('title')
    reserved = data.get('reserved')
    mystery.title = title if title else mystery.title
    mystery.reserved = reserved if reserved else mystery.reserved
    db.session.commit()
    return mystery_schema.jsonify(mystery)


@app.route('/api/1/<mystery_id>', methods=['DELETE'])
def delete_mystery(mystery_id):
    mystery = MysteryModel.query.get(mystery_id)
    db.session.delete(mystery)
    db.session.commit()
    return mystery_schema.jsonify(mystery)


if __name__ == '__main__':
    app.run(debug=True)
