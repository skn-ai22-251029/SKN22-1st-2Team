
# 요금 정보 가져오기
import traceback
from models.charge_price import ChargePrice
from repository.db import get_connection


def select_charger_price(operator_code: str = ""):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charge_price
             where operator_code = %s
                """
            try:
                cursor.execute(sql, [operator_code,])
                datas = cursor.fetchall()
                prices = []
                for data in datas:
                    prices.append(ChargePrice(*data))

                return prices
            except Exception as e:
                print(e)
                print(traceback.format_exception)
