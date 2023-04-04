#!/usr/bin/python3
"""Comment cities"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state(state_id=None):
    """Return cities by state"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        all_cities = storage.all('City')
        state_cities = [city.to_dict() for city in all_cities.values()
                        if city.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        if data.get("name") is None:
            abort(400, 'Missing name')

        data['state_id'] = state_id
        new_state = City(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_by_id(city_id=None):
    """City by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        del city
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400, 'Not a JSON')
        for key, val in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        city.save()
        return jsonify(city.to_dict()), 200
