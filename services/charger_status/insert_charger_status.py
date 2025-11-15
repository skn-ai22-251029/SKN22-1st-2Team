
# save - 충전기 상태 정보 (charger_status)

import traceback
from models.charger_status import Charger_status
from repository.db import get_connection


def insert_charger_status(charger_status: Charger_status):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_status 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                    stat        = %s,
                    stat_upd_dt = %s,
                    last_tsdt   = %s,
                    last_tedt   = %s,
                    now_tsdt    = %s,
                    reg_dt      = %s,
                    upd_dt      = NOW()
            """

            params = (*charger_status.as_tuple(), 
                    charger_status.stat,
                    charger_status.stat_upd_dt,
                    charger_status.last_tsdt,
                    charger_status.last_tedt,
                    charger_status.now_tsdt,
                    charger_status.reg_dt
                      )
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())
                