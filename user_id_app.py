import gspread
import sys
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials
users = list()

#index   0    1
#taget date  id

def check_user(user_id):
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).sheet1
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
        global users
        users = worksheet.col_values(2)
        print('複製已存在的users' ,GSpreadSheet)
        if user_id in users:
            print("已存在使用者")
            return users.index(user_id) + 1
        else:
            users.append(user_id)
            worksheet.append_row((json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), user_id))
            print("已新增使用者")
            return -1
    