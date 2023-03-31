#!/usr/bin/python3
"""create a new view for State objects
that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    """return a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_count():
    """return the number of states"""
    from models.state import State
    from models.city import City
    from models.user import User
    from models.place import Place
    from models.review import Review
    from models.amenity import Amenity
    classes = {Amenity: "amenities",
               City: "cities",
               Place: "places",
               Review: "reviews",
               State: "states",
               User: "users"}
    return jsonify({name: storage.count(cls) for cls, name in classes.items()})
