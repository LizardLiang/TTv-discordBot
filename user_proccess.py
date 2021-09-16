import gspread
import sys
import datetime
import json
from oauth2client.service_account import ServiceAccountCredentials

user_id = list()
user_status = list()

def connect_to_spread():
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
            key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet = gc.open(GSpreadSheet).worksheet('users')
            return worksheet
        except Exception as ex:
            print('無法連線Google試算表', ex)
            sys.exit(1)
            
def user_index(_id, worksheet):
    worksheet = connect_to_spread()
    global user_id
    user_id = worksheet.col_values(1)
    global user_status
    user_status = worksheet.col_values(2)
    if _id not in user_id:
        row_to_add = [_id, 0]
        worksheet.append_row(row_to_add)
        user_id.append(_id)
        user_status.append(0)
    return user_id.index(_id)

def check_status(_id, worksheet):
    global user_id
    _index = user_index(_id, worksheet)
    _status = user_status[_index]
    return _status

def set_status(_id, status, worksheet):
    _index = user_index(_id, worksheet)
    user_status[_index] = 1
    worksheet.update_cell(_index+1, 2, str(status))
    return 'set ' + _id + 'to search'

def clear_status(_id, worksheet):
    _index = user_index(_id, worksheet)
    user_status[_index] = 0
    worksheet.update_cell(_index+1, 2, '0')
    return 'set ' + _id + 'to normal'

def set_theater(_id, _url_k, worksheet):
    _index = user_index(_id, worksheet)
    worksheet.update_cell(_index+1, 3, _url_k)
    print('set theater success')
    
def read_theater(_id, worksheet):
    _index = user_index(_id, worksheet)
    print('index: ', _index)
    url_k_1 = worksheet.cell(_index+1, 3).value
    return url_k_1