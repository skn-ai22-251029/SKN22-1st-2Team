import traceback
from typing import Optional

from models.charger_station import Charger_station
from repository.db import get_connection


def select_charger_station(id: str = "") -> Optional[list]:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charger_station
"""
            if id != "":
                sql += "where station_id = " + id

            try:
                cursor.execute(sql)
                datas = cursor.fetchall()
                stations = []
                for data in datas:
                    stations.append(Charger_station(*data))

                return stations
            except Exception as e:
                print(e)
                print(traceback.format_exception)


def select_charger_station_location(lat: float, lng: float) -> Optional[list]:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
        select  station_id, station_name, addr, addr_detail, location, lat, lng,
                use_time, parking_free, note, limit_yn, limit_detail, del_yn,
                del_detail, kind, kind_detail, zcode, zscode, traffic_yn, year,
                floor_num, floor_type, operator_id, update_dt
          from  (
            select  station_id, station_name, addr, addr_detail, location, lat, lng,
                    use_time, parking_free, note, limit_yn, limit_detail, del_yn,
                    del_detail, kind, kind_detail, zcode, zscode, traffic_yn, year,
                    floor_num, floor_type, operator_id, update_dt,
                   ( 6371 * ACOS( COS(RADIANS(%s)) * COS(RADIANS(lat)) *
                                  COS(RADIANS(lng) - RADIANS(%s)) +
                                  SIN(RADIANS(%s)) * SIN(RADIANS(lat)))) AS distance_km
              from charger_station
            HAVING distance_km <= 5
            ) a
"""

            try:
                cursor.execute(sql, [lat, lng, lat])
                datas = cursor.fetchall()
                return [Charger_station(*data) for data in datas]
            except Exception as e:
                print(e)
                print(traceback.format_exception)

def select_all_charger_station() :
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charger_station
"""
            try:
                cursor.execute(sql)
                datas = cursor.fetchall()
                stations = []
                for data in datas:
                    stations.append(Charger_station(*data))

                return stations
            except Exception as e:
                print(e)
                print(traceback.format_exception)