#!/usr/bin/python3
"""First api with flask and python"""

import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
Swagger(app)  # allow swagger

app.register_blueprint(app_views)
CORS(app, resources=r"/api/v1/*", origins="*")
app.url_map.strict_slashes = False  # allow /api/v1/states/ and /api/v1/states

host = os.getenv("HBNB_API_HOST", "0.0.0.0")
port = os.getenv("HBNB_API_PORT", 5000)


@app.errorhandler(404)
def error(self):
    """404 error but return empty dict"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(*args, **kwargs):
    """close storage"""
    storage.close()

#allow cross-origin for all routes and methods


@app.after_request  # after request
def after_request(response):
    """allow cross-origin for all routes and methods"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Accept'] = '*/*'
    return response


if __name__ == "__main__":
    """Flask Boring App"""
    # print(app.url_map)
    app.run(host=host, port=port)
