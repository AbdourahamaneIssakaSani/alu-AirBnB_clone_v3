#!/usr/bin/python3
"""new view for RESTful api actions
link place and amenities"""

from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == 'db':
    @app_views.route('/places/<place_id>/amenities', strict_slashes=False)
    def get_amenities_by_placeid(place_id):
        '''get amenities'''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_amenity(place_id, amenity_id):
        '''delete an amenity'''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity(place_id, amenity_id):
        '''create an amenity'''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

if storage_type == 'fs':
    @app_views.route('/places/<place_id>/amenities', strict_slashes=False)
    def get_allamenities(place_id):
        '''get amenities'''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_amenity(place_id, amenity_id):
        '''delete an amenity'''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200


    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity(place_id, amenity_id):
        '''create an amenity'''
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
