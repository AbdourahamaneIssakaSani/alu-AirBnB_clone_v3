#!/usr/bin/python3
"""a new view that handles RESTful Api actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_allamenities():
    """retrieves all amenities"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return jsonify(amenities), 200


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def create_amenities():
    """create amenities"""
    amenities = storage.all(Amenity).values()
    amenities_data = request.get_json()
    if not amenities_data:
        return jsonify({'error': 'Not a JSON'})
    if 'name' not in amenities_data:
        return jsonify({'error': 'Missing name'})
    amenities_data.pop('id', None)
    amenities_data.pop('created_at', None)
    amenities_data.pop('updated_at', None)
    for amenity in amenities:
        if amenity:
            if amenity.name == amenities_data['name']:
                setattr(amenity, 'name', amenities_data['name'])
                amenity.save()
                return jsonify(amenity.to_dict()), 200
    amenity = Amenity(**amenities_data)
    amenity = storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity_actions(amenity_id):
    """actions on amenities"""
    if request.method == 'GET':
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict()), 200

    if request.method == 'DELETE':
        """delete an amennity"""
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        """update an amenity"""
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        amenity_data = request.get_json()
        if not amenity_data:
            return jsonify({'error': 'Not a JSON'})
        for key, value in amenity_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
