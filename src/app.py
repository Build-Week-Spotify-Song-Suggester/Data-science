import pandas as pd
import json
import requests
from flask import Flask, \
    request, \
    jsonify
from flask_cors import CORS
import sqlite3
import os

DB_FILE = 'db.sqlite3'


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    CORS(app)

    def create_connection(db_file, verbose=False):
        """
        Create a database connection to a SQLite3 database

        Parameter
        --------------------------------------------------------
        db_file: str
                    database file path
        verbose: bool
                    prints detail output of connection

        Returns
        --------------------------------------------------------
        conn : sqlite3.Connection
                    returns sqlite3 connection object
        """
        # Check if db_file path is valid
        if not os.path.isfile(db_file):
            raise IOError(f'Invalid database file path: {db_file}')

        conn = None
        try:
            conn = sqlite3.connect(db_file)
            if verbose:
                print(f'Using SQLite version: {sqlite3.version}')
                print(f'Creating Connection to {db_file}...')
            return conn
        except sqlite3.Error as e:
            print(e)

    def select_query(conn, query, verbose=False):
        """
        Queries and returns results from the database as Pandas DataFrame

        Parameter
        -------------------------------------------------------
        conn : sqlite3.Connection
                    returns sqlite3 connection object
        query : String
                    SQL SELECT query
        verbose: bool
                    prints detail output of connection

        Returns
        --------------------------------------------------------
        results : DataFrame
                    returns results as Pandas DataFrame
        """
        if not query.startswith('SELECT'):
            raise ValueError('Query should begin with `SELECT`')

        df = pd.read_sql(query, conn)

        if verbose:
            print(df.head())
        return df

    @app.route('/')
    def index():
        return "Spotifier Recommender API is Working"

    @app.route('/api', methods=['POST'])
    def api():

        data_in = request.get_json(force=True)

        try:
            # Create db connection
            conn = create_connection(DB_FILE, verbose=True)

            try:
                # Get track id of searched song
                track_id = data_in["Searched_Song"]
            except Exception as e:
                return f"Index Error for: {data_in}, make sure parameters passed are correct."

            # Find similar songs
            query = "SELECT * FROM recommendations WHERE Searched_Song == '{}'".format(
                track_id)

            similar_songs = select_query(conn, query)

            return jsonify(similar_songs.to_dict(orient='records')[0])

        except Exception as e:
            print(e)
            return f"Can't find the {track_id}"

    return app
