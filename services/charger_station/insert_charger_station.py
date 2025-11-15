
# save - 충전소 기본 정보(charger_station)

import traceback
from models.charger_station import Charger_station
from repository.db import get_connection


def insert_station(station:Charger_station):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_station 
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                use_time     = %s,
                limit_yn     = %s,
                limit_detail = %s,
                del_yn       = %s,
                del_detail   = %s,
                update_dt    = NOW()
            """
            params = (*station.as_tuple(), station.use_time, station.limit_yn, station.limit_detail, station.del_yn, station.del_detail)
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())