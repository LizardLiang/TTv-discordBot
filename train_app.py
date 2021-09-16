from bs4 import BeautifulSoup
import requests

def train(string_1):
    URL = "https://tw.piliapp.com/%E5%8F%B0%E9%90%B5%E7%81%AB%E8%BB%8A%E6%99%82%E5%88%BB%E8%A1%A8/?q="
    URL = URL + string_1
    res = requests.get(URL)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text,'html.parser')
    articles = soup.find_all('td')
    text = list()
    for num_1 in range(len(articles)):
        if "訂票" == articles[num_1].text or '' == articles[num_1].text or " " in articles[num_1] or '小時' in articles[num_1].text:
            continue
        text.append(articles[num_1].text)
    for num_2 in range(len(text)):
        text[num_2] = text[num_2] + "\n"
    return text