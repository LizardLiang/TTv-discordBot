import gspread
import sys
import datetime
import json, random
from oauth2client.service_account import ServiceAccountCredentials
porns = list()


def load_porn():
    GDriveJSON = 'FAMAX-ef61fdf82b20.json'
    GSpreadSheet = 'line-bot'
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        key = ServiceAccountCredentials.from_json_keyfile_name(GDriveJSON, scope)
        gc = gspread.authorize(key)
        worksheet = gc.open(GSpreadSheet).worksheet('工作表3')
    except Exception as ex:
        print('無法連線Google試算表', ex)
        sys.exit(1)
    global porns
    porns = worksheet.col_values(2)
    print("porns", porns)
    return worksheet
            
def add_porn(porn_url):
    worksheet = load_porn()
    if porn_url in porns:
        return "exist"
    else:
        porns.append(porn_url)
        worksheet.append_row((json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str), porn_url))
        print('已新增url')
        return 'success'
    
def row_porn():
    load_porn()
    index = random.randint(0, len(porns) - 1)
    return porns[index]