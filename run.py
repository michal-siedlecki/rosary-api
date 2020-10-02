import json
import secrets
from flask import request, redirect, abort, render_template


from models import MysteryModel, mysteries_schema, PrayerModel
from config import app, db

API_URL = '/api/1'


# :::::::::::::::::: LOGIC :::::::::::::::::::::::::::::::::::


def get_prayer(endpoint):
    prayer = PrayerModel.query.filter_by(endpoint=endpoint).first()
    if not prayer:
        abort(404, description="Resource not found")

    PrayerModel.delete_expired(timestamp=prayer.timestamp, duration_days=prayer.duration_days)
    if not prayer:
        abort(404, description="Resource not found")

    result = MysteryModel.query.filter_by(prayer_id=prayer.id)

    return result


def create_prayer(parts, duration):

    with open('rosary.json', 'r') as f:
        rosary = json.load(f)

    endpoint = str(secrets.token_urlsafe(12))
    prayer = PrayerModel(endpoint=endpoint, duration_days=duration)
    db.session.add(prayer)
    db.session.commit()

    for part in parts:
        for m in rosary.get(part):
            mystery = MysteryModel(title=m, prayer_id=prayer.id)
            mystery.prayer_endpoint = endpoint
            prayer.mysteries.append(mystery)
            db.session.add(prayer)
            db.session.commit()

    return endpoint


def update_mystery(prayer_endpoint, mystery_id, http_request):
    prayer = PrayerModel.query.filter_by(endpoint=prayer_endpoint).first()
    if not prayer:
        abort(404, description="Resource not found")
    mystery = MysteryModel.query.get(mystery_id)
    if mystery not in prayer.mysteries:
        abort(404, description="Resource not found")
    data = http_request.get_json(force=True)
    reserved = data.get('reserved')
    mystery.reserved = reserved
    db.session.add(mystery)
    db.session.commit()
    return True


def reserve_mystery(prayer_endpoint, mystery_id):
    prayer = PrayerModel.query.filter_by(endpoint=prayer_endpoint).first()
    if prayer:
        mystery = MysteryModel.query.filter_by(id=mystery_id).first()
        mystery.reserved = True if not mystery.reserved else False
        db.session.add(mystery)
        db.session.commit()
        return True
    abort(404, description="Resource not found")


# :::::::::::::::::: FRONTEND VIEWS ::::::::::::::::::::::::::

@app.route('/')
def views_index():
    return render_template('index.html')


@app.route('/create-prayer', methods=['POST'])
def views_create_prayer():
    mysteries_list = ['radosne', 'bolesne', 'chwalebne', 'swiatla']
    parts = [x for x in mysteries_list if x in request.form]
    duration = request.form.get('dayRange')
    prayer_endpoint = create_prayer(parts, duration)
    return redirect(prayer_endpoint)


@app.route('/<endpoint>', methods=['GET'])
def views_prayer(endpoint):
    mysteries = get_prayer(endpoint)
    return render_template('prayer.html', data=mysteries)


@app.route('/<prayer_endpoint>/<mystery_id>/reserve')
def views_reserve_mystery(prayer_endpoint, mystery_id):
    reserve_mystery(prayer_endpoint,mystery_id)
    return redirect(request.url_root + prayer_endpoint)


# :::::::::::::::::: API VIEWS ::::::::::::::::::::::::::


@app.route(API_URL + '/<endpoint>', methods=['GET'])
def api_get_prayer(endpoint):
    result = get_prayer(endpoint)
    return mysteries_schema.jsonify(result)


@app.route(API_URL, methods=['POST'])
def api_create_prayer():
    parts = request.get_json(force=True).get('parts')
    duration = request.get_json(force=True).get('duration')
    endpoint = create_prayer(parts, duration)
    return redirect(request.url + '/' + endpoint, code=302)


@app.route(API_URL + '/<prayer_endp>/<mystery_id>', methods=['PATCH'])
def api_update_mystery(prayer_endp, mystery_id):
    return update_mystery(prayer_endp, mystery_id, request)


if __name__ == '__main__':
    app.run(debug=True)
