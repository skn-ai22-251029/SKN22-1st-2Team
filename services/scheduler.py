import schedule
import time

from models.charger_detail import Charger_detail
from models.charger_station import Charger_station
from models.charger_status import Charger_status
from services.api.get_charger_data import EVChargerAPI
from services.charger_detail import insert_charger_detail
from services.charger_station import insert_charger_station
from services.charger_status import insert_charger_status


def job():
    getAPI = EVChargerAPI()
    # 일부 정보 조회
    chargers_info = getAPI.get_charger_info()
    
    # 전체 정보 조회
    # chargers_info = getAPI.get_all_charger_info()

    if chargers_info:
        stations = [Charger_station.from_dto(dto) for dto in chargers_info]
        for station in stations:
            print(station)
            insert_charger_station(station)

    # 일부 정보 조회
    chargers_status_dtos = getAPI.get_charger_status()
    
    # 전체 정보 조회
    # chargers_status_dtos = getAPI.get_all_charger_status()
    
    if chargers_status_dtos:
        chargers_status = [Charger_status.from_dto(dto) for dto in chargers_status_dtos]

        for charger_status in chargers_status:
            print(charger_status)
            insert_charger_status(charger_status)


    if chargers_info and chargers_status_dtos:
        charger_details = []

        # statId + chgerId 기준으로 매칭
        for info_dto in chargers_info:
            for stat_dto in chargers_status_dtos:
                if info_dto.statId == stat_dto.statId and info_dto.chgerId == stat_dto.chgerId:
                    detail = Charger_detail.from_dtos(info_dto, stat_dto)
                    charger_details.append(detail)
                    break
        
        for detail in charger_details:
            print("[DETAIL]", detail.station_id, detail.charger_id, detail.stat)
            insert_charger_detail(detail)    

