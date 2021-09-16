import requests, json
from bs4 import BeautifulSoup

def find_plane(message):
    """
    #單程
    url = 'https://www.expedia.com.tw/Flights-Search?trip=oneway&leg1=from%3A'出發機場'%2Cto%3A'到達機場'%2Cdeparture%3A'出發日期'TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=cabinclass%3Aeconomy&mode=search&origref=www.expedia.com.tw'
    #來回
    url = 'https://www.expedia.com.tw/Flights-Search?trip=roundtrip&leg1=from%3A'出發機場'%2Cto%3A'到達機場'%2Cdeparture%3A'出發日期'TANYT&leg2=from%3A'出發機場'%2Cto%3A'到達機場'%2Cdeparture%3A'時間'TANYT&passengers=adults%3A成人人數%2Cchildren%3A兒童人數%2Cseniors%3A年長者人數%2Cinfantinlap%3AY&options=cabinclass%3A艙等&mode=search&origref=www.expedia.com.tw'
    """
    r = requests.get('https://www.expedia.com.tw/Flights-Search?trip=roundtrip&leg1=from%3A%E6%9D%B1%E4%BA%AC%2C%20%E6%97%A5%E6%9C%AC%20(TYO)%2Cto%3A%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3%20(TPE)%2Cdeparture%3A2019%2F03%2F28TANYT&leg2=from%3A%E5%8F%B0%E5%8C%97%2C%20%E5%8F%B0%E7%81%A3%20(TPE)%2Cto%3A%E6%9D%B1%E4%BA%AC%2C%20%E6%97%A5%E6%9C%AC%20(TYO)%2Cdeparture%3A2019%2F04%2F24TANYT&passengers=adults%3A1%2Cchildren%3A0%2Cseniors%3A0%2Cinfantinlap%3AY&options=carrier%3A%E5%9C%8B%E6%B3%B0%E8%88%AA%E7%A9%BA%2Ccabinclass%3Aeconomy&mode=search&origref=www.expedia.com.tw')
    web = BeautifulSoup(r, 'html.parser')