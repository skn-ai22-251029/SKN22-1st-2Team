# save - charge_price(요금정보)

import traceback
from models.charge_price import ChargePrice
from repository.db import get_connection


def insert_charger_price(charge_price: ChargePrice):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charge_price 
            values (
                %s, %s, %s, %s, %s, %s, %s,%s)
            ON DUPLICATE KEY UPDATE
                    guest_price=%s,
                    update_dt=now()
            """
            params =(*charge_price.as_tuple(),charge_price.guest_price)
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())