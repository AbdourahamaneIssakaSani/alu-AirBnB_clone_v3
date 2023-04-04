#!/usr/bin/python3
"""first api with flask and python"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask('v1')

app.register_blueprint(app_views)
CORS(app, resources=r"/api/v1/*", origins="*")
app.url_map.strict_slashes = False  # allow /api/v1/states/ and /api/v1/states
host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')
threaded = True if getenv('HBNB_API_HOST') else False


@app.errorhandler(404)
def error(self):
    """404 error but return empty dict"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(*args, **kwargs):
    """close storage"""
    storage.close()


if __name__ == "__main__":
    if host is None:
        HBNB_API_HOST = '0.0.0.0'
    if port is None:
        HBNB_API_PORT = 5000
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=threaded)
