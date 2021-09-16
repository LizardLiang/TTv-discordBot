import requests, json, hmac, base64
from lxml import etree
from hashlib import sha1
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from pprint import pprint

app_id = '5b0874b66c94481289e4d20efec3ab24'
app_key = '4Fw377NVqLHNRt6b_ypYoDB0iqI'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }

def find_bus(bus_name, stop_name):
    a = Auth(app_id, app_key)
    """
    url_time = 'https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taipei/' + bus_name + '?$format=JSON'
    url_route = 'https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei/' + bus_name + '?$format=JSON'
    url_info = 'https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei/' + bus_name + '?$format=Json'
    
    a = Auth(app_id, app_key)
    # 抓預估到站時間
    response = requests.get(url_time, headers= a.get_auth_header())
    # 抓路線圖
    response_1 = requests.get(url_route, headers= a.get_auth_header())
    #抓公車資訊
    response_info = requests.get(url_info, headers= a.get_auth_header())
    data = json.loads(response.content)
    #data_1 = json.loads(response_1.content)
    data_info = json.loads(response_info.content)
    """
    data = check_region(bus_name, 'https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City', a)
    data_info = check_region(bus_name, 'https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City', a)
    stop_1st = data_info[0]["DepartureStopNameZh"]
    stop_last = data_info[0]["DestinationStopNameZh"]
    print(stop_1st, stop_last)
    reply = ""
    reply += '往 ' + stop_last + '\n'
    #stops_0 = data_1[0]['Stops'] #路線圖的stops
    reply += set_time(data, stop_name, 0)
    reply += '往 ' + stop_1st + '\n'
    reply += set_time(data, stop_name, 1)
    return reply
    
   

def set_time(data, stop_name, index):
    reply = ""
    for d_1 in data:
            try:
                if d_1['Direction'] == index and d_1['StopName']['Zh_tw'] == stop_name:
                    r_min = d_1['EstimateTime'] / 60
                    reply += d_1['StopName']['Zh_tw'] + '(' + str(round(r_min, 1)) + ")min\n"
                    return reply
            except ValueError:
                print(ValueError)
            except :
                if d_1['Direction'] == index and d_1['StopName']['Zh_tw'] == stop_name:
                    reply += d_1['StopName']['Zh_tw'] + '(公車未發車)' + "\n"
                    return reply
    
def check_region(bus_name, url_part, a):
    url = url_part + '/Taipei/' + bus_name + '?$format=JSON'
    response = requests.get(url, headers= a.get_auth_header())
    data = json.loads(response.content)
    if len(data) < 1:
        url = url_part + '/NewTaipei/' + bus_name + '?$format=JSON'
        response = requests.get(url, headers= a.get_auth_header())
        data = json.loads(response.content)
        print('change')
    return data
