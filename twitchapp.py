import requests, json
from bs4 import BeautifulSoup

def get_streams(twitchid):
    id = twitchid.split(' ')
    header = {'Client-ID': "tudijxjlggseb3k0gwfy8jwoiach9z"}
    r = requests.get("https://api.twitch.tv/helix/streams?user_login=" + id[1], headers = header)
    r_1 = json.loads(r.content)
    r_2 = r_1["data"]
    if len(r_2) != 0:
        r_3 = r_2[0]
        if r_3['type'] ==  'live':
            return 'https://www.twitch.tv/' + id[1] + '\n' + id[1] + ' is currently streaming' 
    else:
        return 'https://www.twitch.tv/' + id[1] + '\n' + id[1] + ' is currently offline'
