#https://www.ptt.cc/bbs/Beauty/index.html
import requests, datetime
from bs4 import BeautifulSoup

def get_ptt(url):
    date = datetime.datetime.now().date()
    date_t = date.strftime("%Y-%m-%d")
    date_l = date_t.split('-')
    date_m = int(date_l[1])
    date_d = int(date_l[2])
    print(date_m, date_d)

    r = requests.get(url)
    r_1 = BeautifulSoup(r.content, 'html.parser')
    next_page = r_1.find_all('a', string = '‹ 上頁')
    n_p_url = next_page[0]['href']
    r_2 = r_1.find_all('div', {'class': 'r-ent'})
    for r_3 in r_2:
        r_4 = r_3.find_all('div', class_ = 'date')
        print(r_4.parent())
    url_pre = "https://www.ptt.cc"
    print(url, url_pre + n_p_url)


if __name__ == '__main__':
    get_ptt("https://www.ptt.cc/bbs/Beauty/index.html")