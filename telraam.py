from datetime import datetime, timedelta
import os

import requests
from joblib import Memory

cachedir = '.cache'
memory = Memory(cachedir, verbose=0)

headers = {'X-Api-Key': os.environ['TELRAAM_API_KEY'],
           'Content-Type': 'application/json'}


@memory.cache
def all_segments():
    url = "https://telraam-api.net/v1/segments/all"
    return requests.get(url, headers=headers).json()


@memory.cache
def traffic_snapshot():
    url = "https://telraam-api.net/v1/reports/traffic_snapshot"
    data = {'time': 'live',
            'contents': 'minimal',
            'area': 'full'}
    return requests.post(url, data, headers=headers).json()


def traffic(segment_id):
    url = "https://telraam-api.net/v1/reports/traffic"
    now = datetime.now()
    end = now - timedelta(days=now.weekday())
    start = end - timedelta(weeks=11)

    data = {"level": "segments",
            "format": "per-hour",
            "id": segment_id,
            "time_start": start,
            "time_end": end
            }
    print(data)
    return requests.post(url, data, headers=headers).json()
