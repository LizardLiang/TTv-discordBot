import requests
import json
from bs4 import BeautifulSoup

def e_report():
    r = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-34B859A6-E135-4A75-A4F7-0C34526588BA")
    r_1 = json.loads(r.content)
    return r_1["records"]["earthquake"][0]["reportContent"]