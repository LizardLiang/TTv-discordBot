import gspread
import sys
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials

user_id = list()
user_status = list()

def connect_to_sheet():
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    global worksheet
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).worksheet('theater')
            return worksheet
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
            
def find_theater(keyword, wks):
    theaters = wks.col_values(1)
    code = wks.col_values(2)
    for theater_t in theaters:
        if keyword in theater_t:
            return code[theaters.index(theater_t)]
    return '-1'

def list_theater(wks):
    theaters = wks.col_values(1)
    t_1 = ''
    for t in theaters:
        t_1 += t + '\n'
    return t_1