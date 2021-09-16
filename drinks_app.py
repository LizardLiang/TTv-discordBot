import gspread
import sys
import datetime
import json
import random
from oauth2client.service_account import ServiceAccountCredentials
drinks = list()

def add_drinks(drink_name, user_id):
    d_index = check_drinks(drink_name, user_id)
    print("d_index", d_index)
    if d_index == -1:
        return -1
    else:
        return 0
    
    
def check_drinks(drink_name, user_id):
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).worksheet("工作表2")
    except Exception as ex:
        print('無法連線Google試算表', ex)
        sys.exit(1)
    global drinks
    drinks = worksheet.col_values(2)
    for drink_cnt in drinks:
        if drink_name == drink_cnt:
            print("exist")
            return drinks.index(drink_name)
    print("added")
    worksheet.append_row((json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), drink_name, user_id))
    return -1
            
def random_drinks():
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).worksheet("工作表2")
    except Exception as ex:
        print('無法連線Google試算表', ex)
        sys.exit(1)
    global drinks
    drinks = worksheet.col_values(2)
    if len(drinks) != 0:
        max_index = len(drinks) - 1
        index = random.randint(0, max_index)
        return drinks[index]
    return "nothing here"