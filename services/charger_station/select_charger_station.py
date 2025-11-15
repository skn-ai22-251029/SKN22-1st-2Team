
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
            sql += "limit 100"

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
