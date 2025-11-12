# scripts/update_data.py
import os
import requests
from dotenv import load_dotenv


class EVChargerAPI:
    """공공데이터 전기차 충전소 API 핸들러"""

    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("API_BASE_URL")
        self.api_key = os.getenv("API_KEY")

    def _get(self, endpoint: str, params: dict):
        """공통 GET 요청 처리"""
        params["serviceKey"] = self.api_key
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()  # dataType=JSON인 경우

    def get_charger_info(self, sta_id: str = "", chger_id: str = ""):
        """충전기 정보 조회"""
        params = {
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
        }
        if sta_id:
            params["staId"] = sta_id
        if chger_id:
            params["chgerId"] = chger_id

        return self._get("getChargerInfo", params)

    def get_charger_status(self, sta_id: str = "", chger_id: str = ""):
        """충전기 상태 조회"""
        params = {
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
        }
        if sta_id:
            params["staId"] = sta_id
        if chger_id:
            params["chgerId"] = chger_id

        return self._get("getChargerStatus", params)


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
