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


if __name__ == '__main__':
    segments = all_segments()
    with open(os.path.join('data', 'segments.json'), 'w') as f:
        json.dump(segments, f, indent=2)
    now = datetime.now()
    current_week = now - timedelta(days=now.weekday())
    w = os.path.join('data', current_week.strftime('%Y-%m-%d'))
    for segment in segments['features']:
        s_id = segment['properties']['oidn']
        os.makedirs(w, exist_ok=True)
        filepath = os.path.join(w, f"{s_id}.json")
        if os.path.exists(filepath):
            continue
        else:
            data = traffic_last_3_months(s_id)
            print(filepath, len(data))
            if data['message'] == "Limit Exceeded":
                print("Limit Exceeded")
                break
            elif data['message'] == "ok":
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                print("Unknown error", data)
                break
            time.sleep(3)
