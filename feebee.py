import requests, json, jsonparser, re
from lxml import etree


def web_to_json(message):
    if '!' in message:
        item = message.split('!比價')
    else:
        item = message.split('！比價')
    print('item', item[1])
    if ' ' in item[1] and ('<' not in item[1] and '>' not in item[1]):
        item = item[1].split(' ')
        r_url = 'https://feebee.com.tw/s/?q='
        for item_1 in item:
            if item_1 == item[0]:
                r_url += item_1
            else:
                r_url += '+' + item_1
    elif '<' in item[1] or '>' in item[1]:
        max_value = ''
        min_value = ''
        k_word = ''
        r_url = 'https://feebee.com.tw/s/?q='
        try:
            obj = item[1].split('<')
            if '>' in obj[1]:
                obj_1 = obj[1].split('>')
                max_value = obj_1[1]
                min_value = obj_1[0]
                if ' ' in obj[0]:
                    words = obj[0].split(' ')
                    for word in words:
                        if word == words[0]:
                            k_word += word
                        else:
                            k_word += '+' + word
                else:
                    k_word = obj[0]
                r_url += k_word + '&ptab=1&sort=p&mode=l&best=&pl=' + max_value + '&ph=' + min_value
                print('max', obj_1[1], 'min', obj_1[0])
            elif '>' in obj[0]:
                obj_1 = obj[0].split('>')
                if ' ' in obj_1[0]:
                    words = obj_1[0].split(' ')
                    for word in words:
                        if word == words[0]:
                            k_word += word
                        else:
                            k_word += '+' + word
                else:
                    k_word = obj_1[0]
                max_value = obj[1]
                min_value = obj_1[1]
                r_url += k_word + '&ptab=1&sort=p&mode=l&best=&pl=' + min_value + '&ph=' + max_value
                print('max', obj_1[1], 'min', obj_1[0])
            else:
                max_value = obj[1]
                k_word = obj[0]
                r_url += k_word + '&ptab=1&sort=p&mode=l&best=&pl=' + min_value + '&ph=' + max_value
                print('min', obj[1])
        except:
            try:
                obj = item[1].split('>')
                if '<' in obj[1]:
                    k_word = ''
                    obj_1 = obj[1].split('<')
                    min_value = obj_1[1]
                    max_value = obj_1[0]
                    if ' ' in obj[0]:
                        words = obj[0].split(' ')
                        for word in words:
                            if word == words[0]:
                                k_word += word
                            else:
                                k_word += '+' + word
                    else:
                        k_word = obj[0]
                    r_url += k_word + '&ptab=1&sort=p&mode=l&best=&pl=' + min_value + '&ph=' + max_value
                    print('max', max_value, 'min', min_value)
                elif '<' in obj[0]:
                    k_word = ''
                    obj_1 = obj[0].split('<')
                    if ' ' in obj_1[0]:
                        words = obj_1[0]
                        for word in words:
                            if word == words[0]:
                                k_word += word
                            else:
                                k_word += '+' + word
                    else:
                        k_word = obj_1[0]
                    min_value = obj[1]
                    max_value = obj_1[1]
                    r_url += k_word + '&ptab=1&sort=p&mode=l&best=&pl=' + max_value + '&ph=' + min_value
                    print('max', obj_1[1], 'min', obj_1[0])
                else:
                    min_value = obj[1]
                    k_word = obj[0]
                    r_url += k_word + '&ptab=1&sort=p&mode=l&best=&pl=' + min_value + '&ph='
                    print('max', min_value)
            except:
                print('no < and >')
    else:
        r_url = 'https://feebee.com.tw/s/?q=' + item[1]
    print('r_url', r_url)
    r = requests.get(r_url)
    r_1 = etree.HTML(r.text)
    name = r_1.xpath('//li[starts-with(@class, "pure-g")]')
    t = r_1.xpath("//span[starts-with(@class,'price ellipsis xlarge')]|//li[starts-with(@class,'price ellipsis xlarge')]")
    price = ''
    name_l = list()
    price_l = list()
    url_l = list()
    if len(t) == 0:
        return 'no such thing'
    for cnt in range(len(t)-1):
        """
        name_2 = name[cnt].xpath('span')
        name_3 = name_2[0].xpath('a')
        name_4 = name_3[0].attrib['title']
        """
        name_1 = t[cnt].getparent() # -> 找到父標籤
        name_1 = name_1.getparent()
        if cnt == 0 :
            name_1 = name_1.getparent()
            print(name_1)
        try:
            name_1 = name_1.xpath('a')
            url = name_1[0].attrib['href']
            url_s = get_shorten(url)
            url_l.append(url_s)
            name_1 = name_1[0].xpath('string(.)')
            name_1 = name_1.replace('\n', '')
            name_1 = name_1.replace(' ', '')
            name_1 = name_1.replace('價格', '')
        except:
            print('')
        if name_1 != None:
            name_l.append(name_1)
        try:
            price = t[cnt].xpath('string(.)')
            price = price.replace('\n', '')
            price = price.replace(' ', '')
            price = price.replace('價格', '')
            price_l.append(price)
        except:
            print('')
    reply = ''
    if len(price_l) >= 4:
        for cnt in range(4):
            try:
                reply += name_l[cnt] + ' $' +  price_l[cnt] + '\n' + url_l[cnt] + '\n'
            except:
                print('')
    else:
        for cnt in range(len(price_l)):
            try:
                reply += name_l[cnt] + ' $' +  price_l[cnt] + '\n' + url_l[cnt] + '\n'
            except:
                print('')
    print(reply)
    if reply == None:
        reply = 'so such thing'
    return reply
  
def get_shorten(url):
    print('url', url)
    r = requests.post('https://api.pics.ee/v1/links/?access_token=20f07f91f3303b2f66ab6f61698d977d69b83d64', data = {'url':str(url)})
    r_1 = json.loads(r.content)
    print(r_1["data"]["picseeUrl"])
    return r_1["data"]["picseeUrl"]