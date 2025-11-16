
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

def select_all_charger_price():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select *
              from charge_price
             
                """
            try:
                cursor.execute(sql)
                datas = cursor.fetchall()
                prices = []
                for data in datas:
                    prices.append(ChargePrice(*data))

                return prices
            except Exception as e:
                print(e)
                print(traceback.format_exception)

# 지역별 요금 조회 코드. 필요 없을것 같으면 싹 다 삭제. 대신 pages.diff_charger.py도 변경해야함
def select_price_by_region(region: str = ""):
    """
    지역(시도)별 요금 조회
    charger_station.addr의 지역을 추출하고, area_code_master를 통해 zcode를 구함
    charger_status + charge_price를 매칭
    
    Args:
        region (str): 지역명 (예: "서울특별시", "부산광역시")
    
    Returns:
        dict: {운영기관: [ChargePrice, ...]}
    """
    if not region:
        return {}
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                # 지역명으로 zcode 구하기
                cursor.execute("""
                SELECT DISTINCT zcode FROM area_code_master 
                WHERE region = %s
                LIMIT 1
                """, [region])
                zcode_row = cursor.fetchone()
                
                if not zcode_row:
                    print(f"[디버그] 지역 '{region}'에 해당하는 zcode 없음")
                    return {}
                
                zcode = zcode_row[0]
                print(f"[디버그] 지역 '{region}' → zcode: {zcode}")
                
                # zcode로 charger_station 데이터 확인
                cursor.execute("""
                SELECT COUNT(DISTINCT station_id) FROM charger_station 
                WHERE zcode = %s
                """, [zcode])
                station_count = cursor.fetchone()[0]
                print(f"[디버그] zcode={zcode}의 충전소: {station_count}개")
                
                # zcode로 charger_status 데이터 확인
                cursor.execute("""
                SELECT COUNT(DISTINCT station_id) FROM charger_status 
                WHERE station_id IN (
                    SELECT station_id FROM charger_station WHERE zcode = %s
                )
                """, [zcode])
                status_count = cursor.fetchone()[0]
                print(f"[디버그] zcode={zcode}의 charger_status: {status_count}개")
                
                # zcode 기반으로 지역의 요금 조회 (JOIN)
                sql = """
                SELECT DISTINCT cp.*
                FROM charge_price cp
                INNER JOIN charger_status cs ON cp.operator_code = cs.busi_id
                INNER JOIN charger_station cst ON cs.station_id = cst.station_id
                WHERE cst.zcode = %s
                ORDER BY cp.operator_name, cp.price_type_code
                """
                cursor.execute(sql, [zcode])
                datas = cursor.fetchall()
                
                print(f"[디버그] JOIN 결과 행 수: {len(datas)}")
                
                # 운영기관별로 그룹화
                result = {}
                for data in datas:
                    price = ChargePrice(*data)
                    operator = price.operator_name
                    if operator not in result:
                        result[operator] = []
                    result[operator].append(price)
                
                print(f"[디버그] select_price_by_region('{region}'): {len(result)}개 운영기관 반환")
                return result
            
            except Exception as e:
                print(f"[오류] select_price_by_region: {e}")
                print(traceback.format_exc())
                return {}


def select_price_by_station(station_id: str = ""):
    """
    충전소별 요금 조회
    charger_status.busi_id를 통해 charge_price와 매칭
    
    Args:
        station_id (str): 충전소 ID
    
    Returns:
        list: [ChargePrice, ...]
    """
    if not station_id:
        return []
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            SELECT DISTINCT cp.*
            FROM charge_price cp
            INNER JOIN charger_status cs ON cp.operator_code = cs.busi_id
            WHERE cs.station_id = %s
            ORDER BY cp.operator_name, cp.price_type_code
            """
            try:
                cursor.execute(sql, [station_id])
                datas = cursor.fetchall()
                prices = []
                for data in datas:
                    prices.append(ChargePrice(*data))
                return prices
            except Exception as e:
                print(e)
                print(traceback.format_exception)
                return []
