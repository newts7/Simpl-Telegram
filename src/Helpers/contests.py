import json
import requests
from pprint import  pprint
from .url_shortener import get_shorten_url

ALLOWED_PLATFORMS = ['CODECHEF','HACKEREARTH','HACKERRANK','CODEFORCES']

def fetch_contests():
    ongoing = []
    upcoming = []

    response = requests.get('https://contesttrackerapi.herokuapp.com/android/')
    result = response.json()['result']

    for contest in result['ongoing']:
        if contest['Platform'] in ALLOWED_PLATFORMS:
            ongoing.append(contest)

    for contest in result['upcoming']:
        if contest['Platform'] in ALLOWED_PLATFORMS:
            upcoming.append(contest)
    upcoming = upcoming[: 3 if len(upcoming) > 3 else len(upcoming)]
    ongoing = ongoing[: 3 if len(ongoing) > 3 else len(ongoing)]
    return upcoming, ongoing

def frame_message(contests, heading):
    message = '{} contests \n'.format(heading)
    for contest in contests:
        if heading == 'Ongoing':
            message = message + 'Name - {} \nEndtime - {}\nLink - {} \n\n'.format(contest['Name'], contest['EndTime'], get_shorten_url(contest['url']))
        else:
            message = message + 'Name - {} \nStartTime - {}\nEndtime - {}\nLink - {} \n\n'.format(contest['Name'],contest['StartTime'],contest['EndTime'],get_shorten_url(contest['url']))
    return message

def fetch_contests_info():
    upcoming, ongoing = fetch_contests()
    upcoming_message = frame_message(upcoming, 'Upcoming')
    ongoing_message = frame_message(ongoing,'Ongoing')
    return ongoing_message, upcoming_message
