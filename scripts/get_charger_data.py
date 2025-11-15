# scripts/update_data.py
import os
import time
import traceback
from typing import Dict, List, Optional, Union
import requests
from dotenv import load_dotenv

from DTO.charger_info_dto import ChargerInfoDTo
from DTO.charger_stat_dto import ChargerStatDto


class EVChargerAPI:
    """공공데이터 전기차 충전소 API 핸들러"""

    def __init__(self) -> None:
        load_dotenv()
        self.base_url: str = os.getenv("API_BASE_URL", "")
        self.api_key: str = os.getenv("API_KEY", "")

    def _get(self, endpoint: str, params: dict):
        """
        공통 GET 요청 처리
            
        Args:
            endpoint (str): API 엔드포인트
            params (dict): 요청 파라미터

        Returns:
            Optional[List[Dict[str, Any]]]: API 응답 데이터의 item 리스트 또는 None

        """
        params["serviceKey"] = self.api_key
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", {}).get("item", None)
        except Exception as e:
            print(e)
            print(traceback.format_exception)

    def get_charger_info(self, sta_id: str = "", chger_id: str = ""):
        """
        충전기 정보 조회

        Args:
            sta_id (str): 충전소 ID
            chger_id (str): 충전기 ID

        Returns:
            Optional[List[ChargerInfoDTo]]: 충전기 정보 DTO 리스트
        """
        
        params : Dict[str, Union[str, int]] = {
            "pageNo": 1,
            "numOfRows": 99,
            "dataType": "JSON",
        }
        if sta_id:
            params["staId"] = sta_id
        if chger_id:
            params["chgerId"] = chger_id

        result = self._get("getChargerInfo", params)
        if result:
            # JSON의 "null" 문자열을 실제 None으로 변환
            def clean_null(v): return None if v == "null" else v
            cleaned = [{k: clean_null(v) for k, v in item.items()} for item in result]
            return [ChargerInfoDTo(**item) for item in cleaned]
        return None

    def get_charger_status(self, sta_id: str = "", chger_id: str = "") -> Optional[List[ChargerStatDto]]:
        """
        충전기 상태 조회

        Args:
            sta_id (str): 충전소 ID
            chger_id (str): 충전기 ID

        Returns:
            Optional[List[ChargerStatDto]]: 충전기 상태 DTO 리스트
        """
        params: Dict[str, Union[str, int]] = {
            "pageNo": 1,
            "numOfRows": 99,
            "dataType": "JSON",
        }
        if sta_id:
            params["staId"] = sta_id
        if chger_id:
            params["chgerId"] = chger_id

        result = self._get("getChargerStatus", params)
        
        if result:
            return [ChargerStatDto(**item) for item in result]
        return None


    # ----------------------------
    # 전체 조회 (페이지네이션)
    # ----------------------------
    def get_all_charger_info(self) -> List[ChargerInfoDTo]:
        """모든 충전소 정보 전체 조회"""
        all_items = []
        page = 1

        while True:
            params = {
                "pageNo": page,
                "numOfRows": 99,
                "dataType": "JSON",
            }
            result = self._get("getChargerInfo", params)
            if not result:
                break

            def clean_null(v): return None if v == "null" else v
            cleaned = [{k: clean_null(v) for k, v in item.items()} for item in result]
            all_items.extend([ChargerInfoDTo(**item) for item in cleaned])

            print(f"[INFO] ChargerInfo - 페이지 {page} 수집 완료 ({len(result)}건)")
            if len(result) < 99:
                break  # 마지막 페이지 도달
            page += 1
            time.sleep(0.2)  # API RateLimit 방지

        print(f"[완료] 총 {len(all_items)}개 충전소 정보 수집 완료 ✅")
        return all_items

    def get_all_charger_status(self) -> List[ChargerStatDto]:
        """모든 충전기 상태 전체 조회"""
        all_items = []
        page = 1

        while True:
            params = {
                "pageNo": page,
                "numOfRows": 99,
                "dataType": "JSON",
            }
            result = self._get("getChargerStatus", params)
            if not result:
                break

            all_items.extend([ChargerStatDto(**item) for item in result])

            print(f"[INFO] ChargerStatus - 페이지 {page} 수집 완료 ({len(result)}건)")
            if len(result) < 99:
                break
            page += 1
            time.sleep(0.2)

        print(f"[완료] 총 {len(all_items)}개 충전기 상태 수집 완료 ✅")
        return all_items

if __name__ == "__main__":
    api = EVChargerAPI()

    # 테스트용
    # sta_id = "28260005"
    # chger_id = "O2"
    sta_id = ""
    chger_id = ""

    info = api.get_charger_info(sta_id, chger_id)
    status = api.get_charger_status(sta_id, chger_id)

    print("=== 충전기 정보 ===")
    print(info)

    print("\n=== 충전기 상태 ===")
    print(status)
