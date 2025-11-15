
import traceback
from models.charger_status import Charger_status
from repository.db import get_connection


def select_charger_status(id: str = ""):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charger_status
             where station_id = %s
                """
            try:
                cursor.execute(sql, [id,])
                datas = cursor.fetchall()
                status = []
                for data in datas:
                    status.append(Charger_status(*data))

                return status
            except Exception as e:
                print(e)
                print(traceback.format_exception)