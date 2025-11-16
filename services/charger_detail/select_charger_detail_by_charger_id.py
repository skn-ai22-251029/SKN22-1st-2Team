import traceback
from typing import Optional

from models.charger_detail import Charger_detail
from repository.db import get_connection


def select_charger_detail_by_charger_id(charger_id: str) -> Optional[Charger_detail]:
    """충전기 ID(charger_id)로 단일 Charger_detail을 조회합니다.
    일치하는 레코드가 없으면 None을 반환합니다.
    """
    if not charger_id:
        return None

    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            SELECT
                charger_id,
                station_id,
                charger_type,
                output_kw,
                method,
                del_yn,
                del_detail,
                stat,
                stat_upd_dt,
                last_tsdt,
                last_tedt,
                now_tsdt
            FROM charger_detail
            WHERE charger_id = %s
            LIMIT 1
            """
            try:
                cursor.execute(sql, (charger_id,))
                data = cursor.fetchone()
                if not data:
                    return None
                return Charger_detail(*data)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                return None
