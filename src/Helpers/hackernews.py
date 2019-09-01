import requests
import json
from pprint import pprint

def get_top_stories():
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    stories = response.json()
    result = []
    for i in range(min(10, len(stories))):
        response = requests.get('https://hacker-news.firebaseio.com/v0/item/{}.json'.format(stories[i]))
        story = response.json()
        result.append(story)
    return result

