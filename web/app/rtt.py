# @name: rtt.py
# @creation_date: 2023-02-24
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: functions for retrieving data from the RealTimeTrains API
# @acknowledgements:

import os
import base64
import requests
import urllib.request, json

rtt_url = os.environ.get('RTT_URL')
rtt_username = os.environ.get('API_USERNAME')
rtt_password = os.environ.get('API_PASSWORD')

auth = rtt_username + ":" + rtt_password
auth_bytes = auth.encode("ascii")
base64_bytes = base64.b64encode(auth_bytes)
base64_string = base64_bytes.decode("ascii")

payload={}
headers = {"Authorization": "Basic " + base64_string}

def get_departures_single_station(to_station, from_station):
    results = []
    endpoint_url = rtt_url + 'json/search/' + from_station + '/to/' + to_station
    response = requests.request("GET", endpoint_url, headers=headers, data=payload)

    if response.status_code == 200:
        # turn the API response into useful Json
        response = response.json()
        if response['services'] is not None:
            for service in response['services']:
                results.append(service)
        else:
            results = 'None'

    return results

def get_departures_multiple_stations(to_station, from_stations):
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

    return results