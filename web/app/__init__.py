# @name: __init__.py
# @creation_date: 2022-06-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Initialises the app and queries RealTimeTrains
# @acknowledgements:

from flask import Flask, render_template, request
from flask_moment import Moment
import requests
import urllib.request, json
import os
import base64

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():
    rtt_url = os.environ.get('RTT_URL')
    rtt_username = os.environ.get('API_USERNAME')
    rtt_password = os.environ.get('API_PASSWORD')

    auth = rtt_username + ":" + rtt_password
    auth_bytes = auth.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")

    payload={}
    headers = {"Authorization": "Basic " + base64_string}

    to_station = os.environ.get('TO_STATION')
    from_stations = json.loads(os.environ.get('FROM_STATIONS'))

    results = []

    for station in from_stations:
        endpoint_url = rtt_url + 'json/search/' + station + '/to/' + to_station
        response = requests.request("GET", endpoint_url, headers=headers, data=payload)

        if response.status_code == 200:
            # turn the API response into useful Json
            response = response.json()
            for service in response['services']:
                results.append(service)

    results.sort(key=lambda x: x['locationDetail']['realtimeArrival'])

    return render_template('index.html', results=results)
