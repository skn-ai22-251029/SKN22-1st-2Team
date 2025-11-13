
import traceback
from models.charger_station import Charger_station
from models.charger_detail import Charger_detail
from models.charger_status import Charger_status
from repository.db import get_connection


# save - 충전소 기본 정보(charger_station)

def save_station(station:Charger_station):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = f"""
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
                use_time={station[7]},
                limit_yn={station[10]},
                limit_detail={station[11]},
                del_yn={station[12]},
                del_detail={station[13]},
                update_dt=now()
            """
            try:
                cursor.execute(sql, *station)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exception)

# save - 충전소 상세 정보(charger_station)

def save_charger_detail(charger_detail: Charger_detail):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = f"""
            insert into 
                        charger_station 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                charger_type={charger_detail[2]},
                output_kw={charger_detail[3]},
                method  ={charger_detail[4]},
                del_yn={charger_detail[5]},
                del_detail={charger_detail[6]},
                stat={charger_detail[7]},
                stat_upd_dt={charger_detail[8]},
                last_tsdt={charger_detail[9]},
                last_tedt={charger_detail[10]},
                now_tsdt=now()
            """
            try:
                cursor.execute(sql, *charger_detail)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exception)




# save - 충전기 상태 정보 (charger_status)

def save_charger_status(charger_status: Charger_status):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = f"""
            insert into 
                        charger_station 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                stat        = {charger_status[3]},
                stat_upd_dt = {charger_status[4]},
                last_tsdt   = {charger_status[5]},
                last_tedt   = {charger_status[6]},
                now_tsdt    = {charger_status[7]},
                reg_dt      = {charger_status[8]},
                upd_dt      = now()
       
            """
            try:
                cursor.execute(sql, *charger_status)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exception)