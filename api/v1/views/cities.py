#!/usr/bin/python3
"""a new view that handles RESTful Api actions"""

from models import storage
from flask import jsonify, request, abort
# from models.city import City
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities(state_id):
    """retrieves all cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]  # convert to dict
    return jsonify(cities), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_cities(state_id):
    """create new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
        # if request.method == 'POST':
    city_data = request.get_json()
    if not city_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in city_data:
        return jsonify({'error': 'Missing name'}), 400
    city_data.pop('state_id', None)  # remove state_id if it exists
    city_data.pop('id', None)  # remove id if it exists
    city_data.pop('created_at', None)  # remove created_at if it exists
    city_data.pop('updated_at', None)  # remove updated_at if it exists
    for city in state.cities:
        if city:  # if city exists
            if city.name == city_data['name']:
                setattr(city, 'name', city_data['name'])
                city.save()
                return jsonify(city.to_dict()), 200
    city_data['state_id'] = state_id
    city = City(**city_data)  # create new city
    city = storage.new(city)  # add to storage
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_id_city(city_id):
    """retrieves cities using id"""
    if request.method == 'GET':
        cities = storage.get(City, city_id)
        if not cities:
            status = 404
            return jsonify({'error': 'Not found'}), status
        return jsonify(cities.to_dict())
    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if not city:
            status = 404
            return jsonify({'error': 'Not found'}), status
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        city_data = request.get_json()
        if not city_data:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in city_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)  # set attribute
        city.save()  # save to storage
        return jsonify(city.to_dict()), 200
