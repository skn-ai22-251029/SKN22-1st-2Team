import requests
from models.charge_price import ChargePrice
from scripts.save_to_db import save_charger_price



def scrapping_charge_price():
    url = "https://ev.or.kr/nportal/evcarInfo/selectEvcarStationPriceSearch.ajax"

    payload = {
        "spageId": "statsList",
        "srecordCountPerPage": 1000,
        "spageNo": 1,
        "spageSize": 10,
        "excelPage": "",
        "excelCnt": "",
        "bid": "",
        "type": "",
        "selExcelCnt": 1000
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://ev.or.kr/nportal/evcarInfo/initEvcarChargeInfoAction.do"
    }

    res = requests.post(url, data=payload, headers=headers)
    data = res.json()
    charge_datas=data['list']

    
    for charge_data in charge_datas:
        save_charger_price(ChargePrice(*charge_data.values()))
