
# save - 충전소 상세 정보(charger_station)

import traceback
from models.charger_detail import Charger_detail
from repository.db import get_connection


def insert_charger_detail(charger_detail: Charger_detail):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_detail 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                    charger_type = %s,
                    output_kw    = %s,
                    method       = %s,
                    del_yn       = %s,
                    del_detail   = %s,
                    stat         = %s,
                    stat_upd_dt  = %s,
                    last_tsdt    = %s,
                    last_tedt    = %s,
                    now_tsdt     = %s
            """
            params = (*charger_detail.as_tuple(), 
                        charger_detail.charger_type,
                        charger_detail.output_kw,
                        charger_detail.method,
                        charger_detail.del_yn,
                        charger_detail.del_detail,
                        charger_detail.stat,
                        charger_detail.stat_upd_dt,
                        charger_detail.last_tsdt,
                        charger_detail.last_tedt,
                        charger_detail.now_tsdt
                        )
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())

