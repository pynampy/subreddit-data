from datetime import datetime, timedelta
import json


def convert_timestamp_to_human_readable(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    human_readable_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    return human_readable_date


def write_to_json(posts, filename='reddit_posts.json'):
    with open(filename, 'w') as f:
        json.dump(posts, f, indent=4)
