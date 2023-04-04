#!/usr/bin/python3
"""first api with flask and python"""

from flask import Flask, jsonify, make_response
from werkzeug.exceptions import HTTPException
# from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# CORS(app, resources=r"/api/v1/*", origins="*")
app.url_map.strict_slashes = False  # allow /api/v1/states/ and /api/v1/states

app.register_blueprint(app_views)


# threaded = True if getenv('HBNB_API_HOST') else False


@app.errorhandler(404)
def error_not_found(self):
    """404 error but return empty dict"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(*args, **kwargs):
    """close storage"""
    storage.close()


@app.errorhandler(Exception)
def error_global(error):
    """error_global"""
    if isinstance(error, HTTPException):
        if type(error).__name__ == 'NotFound':
            error.description = "Not found"
        message = {'error': error.description}
        code = error.code
    else:
        message = {'error': error}
        code = 500
    return make_response(jsonify(message), code)


if __name__ == "__main__":
    """Flask Boring App"""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")

    print(app.url_map)
    app.run(host=host, port=port)
