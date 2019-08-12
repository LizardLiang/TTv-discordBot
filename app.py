from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from lxml import etree

import requests, threading, sched, time
import random
import datetime
import gspread, sys
from oauth2client.service_account import ServiceAccountCredentials as SAC
import user_id_app, drinks_app, porn_app, movie_app, user_proccess, theater_app, bus_app, train_app, feebee, earthquake, twitchapp
from bs4 import BeautifulSoup
from threading import Timer

groupid = ''

keep_run = True

app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi('eQtj6o0hzXY/7vKiiP1hCzlXN24atMZGzBAG8xSZfDwAINf5yvRK146yUi4OWTJGpe2GbmN2GRdTSpUn6EITDXakjzDHkrVCnSFWygqLY9qAtRWZwbIMwIwm1dhw5ksRdIoUpNW+T78W/k+/4YPmoAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a9d9139f650642a024e4229410567cae')

s = sched.scheduler(time.time, time.sleep)
def do_something(): 
    global keep_run
    cnt = 0
    tw1 = twitchapp
    tw2 = twitchapp
    while keep_run:
        cnt = cnt + 1
        print('checking' + str(cnt))
        state = tw2.get_streams('nana803')
        #if state:
        #    line_bot_api.push_message('U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(state))
        #    time.sleep(10)
            
        state1 = tw1.get_streams('inkwei0108')
        if state and state1:
            message = state + '/n' + state1
            line_bot_api.push_message('U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(message))
        elif state1:
            message = state1
            line_bot_api.push_message('U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(message))
        elif state:
            message = state
            line_bot_api.push_message('U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(message))
        
        # do your stuff
        time.sleep(10)

game_key = 0
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    t.keep_run = False
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global groupid, keep_run
    try:
        groupid = event.source.group_id
        print(event.source.group_id)
    except:
        pass
    pass

@handler.add(JoinEvent)    
def handle_join(event): #加入群組，會回復
    newcoming_text = "恭迎慈孤觀音 渡世靈顯四方"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    t = threading.Thread(target = do_something) #這個就開一個新的thread 讓他自己玩得爽
    t.start()
    app.run(host='0.0.0.0', port=port)