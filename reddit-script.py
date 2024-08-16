import praw
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


def convert_timestamp_to_human_readable(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    human_readable_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    return human_readable_date


def fetch_posts(subreddit_name, limit=1000):
    reddit = praw.Reddit(
        client_id=os.getenv('client_id'),
        client_secret=os.getenv('client_secret'),
        user_agent='script:reddit_data_collector:v1.0.0'
    )

    subreddit = reddit.subreddit(subreddit_name)
    seven_days_ago = datetime.now() - timedelta(days=7)
    cutoff_timestamp = seven_days_ago.timestamp()

    posts = []
    index = 0

    for submission in subreddit.new(limit=limit):
        if submission.created < cutoff_timestamp:
            break

        if submission.author is not None:
            title = submission.title
            title_upper = title.upper()
            if title_upper.startswith('[HIRING]'):
                posts.append({
                    'index': index,
                    'title': submission.title,
                    'body': submission.selftext,
                    'author': submission.author.name,
                    'url': submission.url,
                    'created': convert_timestamp_to_human_readable(submission.created),
                    'created_unix': submission.created
                })
            index += 1

    return posts


def write_to_json(posts, filename='reddit_posts.json'):
    with open(filename, 'w') as f:
        json.dump(posts, f, indent=4)


if __name__ == "__main__":
    subreddit_name = 'forhire'
    posts = fetch_posts(subreddit_name)
    write_to_json(posts)
