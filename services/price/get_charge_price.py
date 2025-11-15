import requests
from models.charge_price import ChargePrice
from services.price import select_charge_price
from services.price.insert_charge_price import insert_charger_price


# 요금정보 크롤링
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
        "selExcelCnt": 1000,
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://ev.or.kr/nportal/evcarInfo/initEvcarChargeInfoAction.do",
    }

    res = requests.post(url, data=payload, headers=headers)
    data = res.json()
    charge_datas = data["list"]

    for charge_data in charge_datas:
        insert_charger_price(ChargePrice(*charge_data.values()))


# 요금정보 계산하여 딕셔너리로 반환
def show_charge_price(operator_code: str = ""):
    prices = select_charge_price(operator_code)

    total_prices = {}
    for price in prices:
        if price.price_type_code == "01":  # 급속 50kWh기준 30분충전
            total_prices["fast"] = int(price.member_price) * 50
        else:  # 완속 7kW기준 4시간 충전시
            total_prices["slow"] = int(price.member_price) * 7 * 4

    return total_prices
