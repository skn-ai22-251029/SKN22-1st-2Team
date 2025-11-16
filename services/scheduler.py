import schedule
import time

from models.charger_detail import Charger_detail
from models.charger_station import Charger_station
from models.charger_status import Charger_status
from services.api.get_charger_data import EVChargerAPI
from services.charger_detail.insert_charger_detail import insert_charger_detail
from services.charger_station.insert_charger_station import insert_station
from services.charger_status.insert_charger_status import insert_charger_status


def job():
    getAPI = EVChargerAPI()
    # 일부 정보 조회
    # chargers_info = getAPI.get_charger_info()

    # 전체 정보 조회
    chargers_info = getAPI.get_all_charger_info()

    if chargers_info:
        stations = [Charger_station.from_dto(dto) for dto in chargers_info]
        for station in stations:
            insert_station(station)

    # 일부 정보 조회
    # chargers_status_dtos = getAPI.get_charger_status()

    # 전체 정보 조회
    chargers_status_dtos = getAPI.get_all_charger_status()

    if chargers_status_dtos:
        chargers_status = [Charger_status.from_dto(dto) for dto in chargers_status_dtos]

        for charger_status in chargers_status:
            insert_charger_status(charger_status)

    if chargers_info and chargers_status_dtos:
        # 최적화: 이중 루프는 O(n*m)으로 매우 느림(대량 데이터에서 불가)
        # 대신 status DTO를 (statId,chgerId) 키로 사전화하고 최신(statUpdDt 기준)만 보관
        start_match = time.time()

        status_map = {}
        for stat_dto in chargers_status_dtos:
            key = (stat_dto.statId or "", stat_dto.chgerId or "")
            # statUpdDt 형식은 YYYYMMDDHHMMSS 문자열이므로 사전 비교로 최신 판별 가능
            existing = status_map.get(key)
            if existing is None:
                status_map[key] = stat_dto
            else:
                # 빈 값 안전 처리
                cur_ts = stat_dto.statUpdDt or ""
                ex_ts = existing.statUpdDt or ""
                if cur_ts > ex_ts:
                    status_map[key] = stat_dto

        # 이제 info 리스트를 순회하며 키 매칭(해당 키에 최신 status가 있으면 조합)
        charger_details = []
        match_count = 0
        for info_dto in chargers_info:
            key = (info_dto.statId or "", info_dto.chgerId or "")
            stat_dto = status_map.get(key)
            if stat_dto:
                detail = Charger_detail.from_dtos(info_dto, stat_dto)
                charger_details.append(detail)
                match_count += 1

        elapsed = time.time() - start_match
        print(f"[INFO] 매칭 완료: info={len(chargers_info)} status_keys={len(status_map)} matches={match_count} (elapsed={elapsed:.2f}s)")

        # DB에 삽입(또는 업데이트)
        for detail in charger_details:
            insert_charger_detail(detail)
