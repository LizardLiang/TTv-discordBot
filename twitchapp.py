import requests, json
from bs4 import BeautifulSoup

status = True

def get_streams(twitchid):
    if ' ' in twitchid:
        id = twitchid.split(' ')
        header = {'Client-ID': "tudijxjlggseb3k0gwfy8jwoiach9z"}
        r = requests.get("https://api.twitch.tv/helix/streams?user_login=" + id[1], headers = header)
        r_1 = json.loads(r.content)
        r_2 = r_1["data"]
        global status
        if len(r_2) != 0:
            r_3 = r_2[0]
            if r_3['type'] == 'live' and not status:
                status = True
                return 'https://www.twitch.tv/' + id[1] + '\n' + r_3['user_name'] + '\n' + r_3['title'] 
        elif len(r_2) == 0 and status:
            status = False
            return 'https://www.twitch.tv/' + id[1] + '\n' + id[1] + ' is currently offline'
    else:
        id = twitchid
        header = {'Client-ID': "tudijxjlggseb3k0gwfy8jwoiach9z"}
        r = requests.get("https://api.twitch.tv/helix/streams?user_login=" + id, headers = header)
        r_1 = json.loads(r.content)
        print('r_1', r_1)
        r_2 = r_1["data"]
        if len(r_2) != 0:
            r_3 = r_2[0]
            if r_3['type'] == 'live' and not status:
                status = True
                return 'https://www.twitch.tv/' + id + '\n' + r_3['user_name'] + '\n' + r_3['title'] 
        elif len(r_2) == 0 and status:
            status = False
            return 'https://www.twitch.tv/' + id + '\n' + id + ' is currently offline'