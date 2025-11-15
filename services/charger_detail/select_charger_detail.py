
import traceback
from models.charger_detail import Charger_detail
from repository.db import get_connection


def select_charger_detail(id: str = ""):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charger_detail
             where station_id = %s
              limit 100
                """
            try:
                cursor.execute(sql, [id,])
                datas = cursor.fetchall()
                detail = []
                for data in datas:
                    detail.append(Charger_detail(*data))

                return detail
            except Exception as e:
                print(e)
                print(traceback.format_exception)
