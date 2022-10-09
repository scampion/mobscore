import json
import time
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


@memory.cache
def traffic(segment_id, start, end):
    url = "https://telraam-api.net/v1/reports/traffic"
    data = {"level": "segments",
            "format": "per-hour",
            "id": str(segment_id),
            "time_start": str(start),
            "time_end": str(end)
            }
    return requests.post(url, data=str(data), headers=headers).json()


def traffic_last_3_months(segment_id):
    now = datetime.now()
    end = now - timedelta(days=now.weekday())
    end = end.replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(weeks=11)
    print(segment_id, start, end)
    return traffic(segment_id, start, end)


def traffic_per_quarter(segment_id, year, quarter):
    start = datetime.strptime(year, '%Y') + (quarter - 1) * timedelta(days=365 / 4)
    end = start + timedelta(days=365 / 4)
    return traffic(segment_id, start, end)


def traffic_last_years(segment_id, years):
    year = datetime.now().year
    for i in range(years):
        for q in range(1, 5):
            yield year - i, q


if __name__ == '__main__':
    segments = all_segments()
    with open(os.path.join('data', 'segments.json'), 'w') as f:
        json.dump(segments, f, indent=2)

    for segment in segments['features']:
        s_id = segment['properties']['oidn']
        for year, quarter in traffic_last_years(s_id, 10):
            jsonpath = os.path.join('data', f'{s_id}_{year}_{quarter}.json')
            if os.path.exists(jsonpath):
                print("Already exists", jsonpath)
                continue
            data = traffic_per_quarter(s_id, str(year), quarter)
            print(year, quarter, data['message'], f'{s_id}_{year}_{quarter}.json', len(data), ' bytes')
            if data['message'] == "ok":
                with open(jsonpath, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                print("Error", data)
            time.sleep(3)
