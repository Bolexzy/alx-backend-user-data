#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)


@app_views.route('/', strict_slashes=False)
def index() -> str:
    ''' GET /
    Return:
        - The home page's payload.
    '''
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
