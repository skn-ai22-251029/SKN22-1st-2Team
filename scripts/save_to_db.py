
import traceback
from models.charger_station import Charger_station
from models.charger_detail import Charger_detail
from models.charger_status import Charger_status
from repository.db import get_connection


# save - 충전소 기본 정보(charger_station)

def save_station(station:Charger_station):
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
            params = (*station, station[7], station[10], station[11], station[12], station[13])
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())

# save - 충전소 상세 정보(charger_station)

def save_charger_detail(charger_detail: Charger_detail):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_station 
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
                    now_tsdt     = NOW()
            """
            params = (*charger_detail, *charger_detail[2:11])
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())




# save - 충전기 상태 정보 (charger_status)

def save_charger_status(charger_status: Charger_status):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_station 
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

            params = (*charger_status, *charger_status[3:9])
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())
                