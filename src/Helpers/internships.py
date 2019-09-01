import  urllib3
from pprint import pprint
from bs4 import  BeautifulSoup
from .url_shortener import get_shorten_url
import random

def parse_has_jobs():
    http = urllib3.PoolManager()
    url = 'https://hasjob.co/?t=intern&c=programming&c=mobile'
    response = http.request('GET', url)
    results = []
    soup = BeautifulSoup(response.data, 'html.parser')
    internship_divs = soup.findAll("a", {"class": 'stickie'})
    for div in internship_divs[1:]:
        internship_url = '{}/{}'.format('https://hasjob.co', div.get('href'))
        headline_tag = div.find('span', {"class": "headline"})
        # pprint(headline_tag.contents[0])
        # pprint(internship_url)
        results.append({
            "title": headline_tag.contents[0],
            "url": internship_url
        })
    return results

def parse_intershala():
    http = urllib3.PoolManager()
    url  = 'https://internshala.com/internships/work-from-home-programming-jobs-in-bangalore,delhi,pune'
    response = http.request('GET', url)
    results = []
    soup = BeautifulSoup(response.data, 'html.parser')
    internship_divs = soup.find_all('div', {'class': "individual_internship_header"})
    for div in internship_divs:
        title = div.find('h4').get('title')
        internship_url = '{}/{}'.format('https://internshala.com/',div.find('a').get('href'))
        results.append({
            "title": title,
            "url": internship_url
        })
    return results

def frame_message(interships):
    message = ''
    for internship in interships:
        message = message + 'Title - {} \n Apply - {}\n\n'.format(internship['title'], get_shorten_url(internship['url']))
    pprint(message)
    return message

def fetch_internships_info():
    intershala_internships = parse_intershala()
    has_jobs_internships = parse_has_jobs()

    interships = has_jobs_internships[
                 : 5 if len(has_jobs_internships) > 5 else len(has_jobs_internships)] + intershala_internships[
                                                                                        : 5 if len(
                                                                                            intershala_internships) > 5 else len(
                                                                                            intershala_internships)]
    random.shuffle(interships)
    return frame_message(interships[: min(5, len(interships))])

# internships=  parse_has_jobs()
# pprint(internships)