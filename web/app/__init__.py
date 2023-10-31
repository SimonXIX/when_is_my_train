# @name: __init__.py
# @creation_date: 2022-06-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Initialises the app and queries RealTimeTrains
# @acknowledgements:

from flask import Flask, render_template, request
from flask_moment import Moment
from .rtt import *
import os
import json

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():
    to_station = os.environ.get('TO_STATION')
    from_stations = json.loads(os.environ.get('FROM_STATIONS'))

    results = rtt.get_arrivals(to_station, from_stations)

    return render_template('index.html', results=results)

@app.route('/coventry')
def coventry():
    to_station = 'COV'
    from_station = 'GLC'

    outbound_results = rtt.get_departures(to_station, from_station)
    return_results = rtt.get_departures(from_station, to_station)

    return render_template('departures.html', outbound_results=outbound_results, return_results=return_results)
