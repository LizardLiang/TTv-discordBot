import requests, json, jsonparser, re
from lxml import etree


def web_to_json():
    r = requests.get('https://feebee.com.tw/s/?q=AIR+PODS')
    r_1 = etree.HTML(r.text)
    name = r_1.xpath('//li[starts-with(@class, "pure-g")]')
    t = r_1.xpath("//span[starts-with(@class,'price ellipsis xlarge')]|//li[starts-with(@class,'price ellipsis xlarge')]")
    price = ''
    name_l = list()
    price_l = list()
    print(len(t), len(name))
    for cnt in range(len(t)-1):
        """
        name_2 = name[cnt].xpath('span')
        name_3 = name_2[0].xpath('a')
        name_4 = name_3[0].attrib['title']
        """
        name_1 = t[cnt].getparent() # -> 找到父標籤
        print(name_1)
        name_1 = name_1.getparent()
        print(name_1)
        if cnt == 0 :
            name_1 = name_1.getparent()
            print(name_1)
        name_1 = name_1.xpath('a')
        name_1 = name_1[0].xpath('string(.)')
        name_1 = name_1.replace('\n', '')
        name_1 = name_1.replace(' ', '')
        name_1 = name_1.replace('價格', '')
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
    print(len(name_l), len(price_l))
    reply = ''
    for cnt in range(len(name_l)-1):
        reply += name_l[cnt] + price_l[cnt] + '\n'
    print(reply)
  