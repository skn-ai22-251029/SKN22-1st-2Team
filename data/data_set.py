from services.charger_detail import select_charger_detail
from services.charger_station import select_charger_station
from services.charger_status import select_charger_status
from services.price import select_charge_price
import pandas as pd 
from dataclasses import asdict

def save_all_to_excel(stations, details, status, prices):
    # 각 객체 리스트를 dict 리스트로 변환
    def to_dict_list(objs):
        return [asdict(o) if hasattr(o, "__dataclass_fields__") else o.__dict__ for o in objs]

    df_station = pd.DataFrame(to_dict_list(stations))
    df_detail = pd.DataFrame(to_dict_list(details))
    df_status = pd.DataFrame(to_dict_list(status))
    df_price = pd.DataFrame(to_dict_list(prices))

    # 여러 시트를 하나의 파일로 저장
    with pd.ExcelWriter("ev_charger_data.xlsx", engine="openpyxl") as writer:
        df_station.to_excel(writer, sheet_name="charger_station", index=False)
        df_detail.to_excel(writer, sheet_name="charger_detail", index=False)
        df_status.to_excel(writer, sheet_name="charger_status", index=False)
        df_price.to_excel(writer, sheet_name="charge_price", index=False)

    print("엑셀 파일로 저장 완료!")

def get_all_data_to_excel():
    charger_station=select_charger_station.select_all_charger_station()
    charger_detail=select_charger_detail.select_all_charger_detail()
    charger_status=select_charger_status.select_all_charger_status()
    charger_price=select_charge_price.select_charger_price()

    save_all_to_excel(charger_station,charger_detail,charger_status,charger_price)

