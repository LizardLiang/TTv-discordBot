from lxml import etree

import requests, re, user_proccess, theater_app

def get_url():
    r = requests.get('http://www.atmovies.com.tw/movie/now/')
    r.encoding = 'big-5'
    r_1 = etree.HTML(r.text)
    r_2 = r_1.xpath('//ul[@class=\"filmListAll2\"]')
    r_3 = r_2[0].xpath('li')
    text = ''
    text_url = ''
    text_1 = list()
    reply_text = ''
    for cnt in range(len(r_3)):
        r_4 = r_3[cnt].xpath('a')
        text_url = etree.tostring(r_4[0])
        text = r_4[0].xpath('text()')
        text_1 += text
        text_1 += "\n"
    reply_text = reply_text.join(text_1)
    return reply_text
        
def get_teaser(movie_name):
    url = 'https://www.youtube.com/user/truemovie1/search?query=' + movie_name
    res = requests.get(url, verify=False)
    r = etree.HTML(res.text)
    r_1 = r.xpath('//a')
    last = None
    for entry in r_1:
        m = re.search("v=(.*)", entry.attrib['href'])
        if m:
            target = m.group(1)
            if target == last:
                continue
            if re.search("list", target):
                continue
            last = target
            return target
    return "failed"
    
def movie_sep(_id, string1, wks_pro):
    t_m = string1.split(' ')
    loc_url = ''
    if len(t_m) <= 0:
        loc_url = user_proccess.read_theater(_id, wks_pro)
    else:
        loc_url = t_m[1]
    t_m_2 = loc_url.split('/')
    timetable_urL = 'http://www.atmovies.com.tw/showtime/'
    timetable_urL += t_m[0] # -> 抓到的電影網址關鍵詞
    timetable_urL += '/' + t_m_2[1] + '/'
    timetable_url = requests.get(timetable_urL) #抓網站
    timetable_text = etree.HTML(timetable_url.text) #把抓到的網站，用HTML的方式轉成文檔
    if loc_url == None:
        timetable = timetable_text.xpath('//a[@href=\"/showtime/t02e13/a02/\"]') #透過這個去反推我要的電影時刻在哪裡
    else:
        timetable = timetable_text.xpath('//a[@href=\"/showtime/' + loc_url + '/\"]')
    reply_text = ""
    result_1 = list()
    for cnt in range(len(timetable)):
        timetable_1 = timetable[cnt].getparent() 
        timetable_2 = timetable_1.getparent() #電影時刻的父標籤
        timetable_3 = timetable_2.xpath('li') #找到時刻的標籤
        for cnt_1 in range(len(timetable_3)):
            result = timetable_3[cnt_1].xpath('text()') #轉為 string -> 但是不知道為啥是 list
            if len(result) != 0 and ' \r\n\t\t\t\t\t\t\t\t' not in result: #去掉空白的跟巨幕廳下面的換行符
                result_1 += result #把 list 合起來
                result_1 += "\n"
    reply_text = reply_text.join(result_1) #把 list 加到 string 裡面
    return reply_text

def find_movie(_id, name, wks_th, wks_pro):
    t_m = name.split(' ')
    loc_url = ''
    if len(t_m) > 1:
        loc_url = theater_app.find_theater(t_m[1], wks_th)
        if loc_url == '-1':
            loc_url = theater_app.find_theater(t_m[0], wks_th)
            t_m_1 = t_m[1]
            if loc_url == '-1':
                return 'find nothing'
        else:
            t_m_1 = t_m[0]
    else:
        loc_url = user_proccess.read_theater(_id, wks_pro)
        t_m_1 = t_m[0]
    if loc_url == None:
        r_1 = requests.get('http://www.atmovies.com.tw/showtime/t02e13/a02/') #讀取樹林秀泰的網頁
    else:
        r_1 = requests.get('http://www.atmovies.com.tw/showtime/' + loc_url + '/') #讀取樹林秀泰的網頁
    r_2 = etree.HTML(r_1.text)
    r_3 = r_2.xpath('//li[@class=\"filmTitle\"]') #讀出所有電影名稱
    for cnt in range(len(r_3)):
        r_4 = r_3[cnt].xpath('a')
        t_1 = r_4[0].xpath('text()') 
        if t_m_1 in t_1: #比較電影名稱
            t_2 = r_4[0].attrib['href']
            t_3 = t_2.split('/')
            return t_3[2] + ' ' + loc_url #有找到的話，回傳網址
        else:
            t_2 = 'find nothing' #沒找到的話，回傳nothing
    return t_2

def buy_ticket(date):
    r_1 = 'https://www.showtimes.com.tw/events?corpId=54'
    if date != 0 :
        r_1 += '&date=' + str(date[1]) + '/' + str(date[2]) + '/' + str(date[3])
    return r_1

def set_location(_id, keyword, wks_th, wks_pro):
    _url = theater_app.find_theater(keyword, wks_th)
    if _url != '-1':
        user_proccess.set_theater(_id, _url, wks_pro)
        return 'set_location success'
    else:
        return '-1'
            