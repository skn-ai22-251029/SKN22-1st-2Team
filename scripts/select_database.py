import traceback
from models import charger_station
from models.charger_detail import Charger_detail
from models.charger_station import Charger_station
from models.charger_status import Charger_status
from models.charge_price import ChargePrice
from repository.db import get_connection


def get_charger_station(id: str = ""):
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


def get_charger_detail(id: str = ""):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charger_detail
             where station_id = %s
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


def get_charger_status(id: str = ""):
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

# 요금 정보 가져오기
def get_charger_price(operator_code: str = ""):
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
