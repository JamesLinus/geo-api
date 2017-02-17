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


# ----------- Hard coded data from example -----------

tasks = [

    {
        'id': 1,
        'title': u'Buy Bowie Albums',
        'description': 'Low, Lodger, Heroes',
        'done': False
    },

    {
        'id': 2,
        'title': u'Mail Bowie Albums',
        'description': 'Josh, Sifu, Nick, James',
        'done': False
    }

]


# ----------- Routes -----------


## ERRORS ##

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

## BROCHURE ##

@app.route('/')
def index():

    the_text = db.metadata

    return render_template('brochure/index.html', the_text=the_text)
## GET ##

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

## POST ##

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task = {
        'id': tasks[-1]['id']+1,
        'title': request.json['title'],
        'description': request.json.get('description'),
        'done': False
    }

    tasks.append(task)
    return jsonify({'task':task}), 201




if __name__ == '__main__':
    app.run(debug=True)

