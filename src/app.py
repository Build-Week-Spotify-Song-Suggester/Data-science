import numpy as np
import pandas as pd
import json
from flask import Flask, \
    render_template, \
    request, \
    jsonify
from flask_cors import CORS
from joblib import load
from sklearn.pipeline import Pipeline


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    CORS(app)
    return app
