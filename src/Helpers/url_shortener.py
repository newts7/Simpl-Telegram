import bitly_api

API_USER = "o_5sklq360vl"
API_KEY = "R_e08b41ae421d436a8a9a35ee17d2d58c"

def get_shorten_url(longUrl):
    client = bitly_api.Connection(API_USER, API_KEY)
    response = client.shorten(uri=longUrl)
    return response['url']
