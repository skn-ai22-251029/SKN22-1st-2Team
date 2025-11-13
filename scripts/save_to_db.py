
import traceback
from models.charger_station import Charger_station
from repository.db import get_connection


def save_station(station:Charger_station):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_station 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
    """
            try:
                cursor.execute(sql, *station)
            except Exception as e:
                print(e)
                print(traceback.format_exception)
            