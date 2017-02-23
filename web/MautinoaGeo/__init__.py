# Flask API example: https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# Flask GeoAlchemy configuration example: https://github.com/flask-admin/flask-admin/blob/master/examples/geo_alchemy/app.py
# Get Flask models to use existing tables for model definitions: http://stackoverflow.com/questions/17652937/how-to-build-a-flask-application-around-an-already-existing-database

# ----------- IMPORTS -----------

# Flask things

from flask import Flask, jsonify, abort, make_response, render_template
from flask_bootstrap import Bootstrap

# SQLAlchemy things
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData, func, case, literal_column
from sqlalchemy.orm import sessionmaker

# Pandas, GeoPandas and GeoAlchemy things

import geopandas as gpd
import geoalchemy2 as geoalch

# ----------- DB and App Setup -----------

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

@app.route('/submit')
def submit():
    return 'This should be the submit response'

if __name__ == '__main__':
    app.run()