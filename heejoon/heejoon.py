# import streamlit as st
# import mysql.connector as mysql

# conn = mysql.connect(
#     host = 'localhost',
#     port = 3306,
#     user = 'skn22',
#     password = 'skn22',
#     database = 'grilled_kim'
# )

# cursor = conn.cursor()

# # 예상대기시간 계산 쿼리 수행
# sql = """
# select
#     *
# from
#     charger_station A join charger_status B
#         on A.station_id = B.station_id join charger_detail C
#             on B.charger_id = C.charger_id join charger_meta D
#                 on C.charger_type = D.charger_type
# """

# cursor.execute(sql)
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# cursor.close()
# conn.close()

"""
class ChargerInfoDTo:
    statNm         : 충전소명               
    statId        : 충전소ID
    chgerId       : 충전기ID
    chgerType     : 충전기타입
    addr          : 주소
    addrDetail     : 주소상세                
    lat            : 위도
    lng            : 경도
    useTime        : 이용가능시간
    busiId        : 기관 아이디
    bnm            : 기관명
    busiNm         : 운영기관명
    busiCall       : 운영기관연락처
    stat          : 충전기상태
    statUpdDt      : 상태갱신일시
    lastTsdt       : 마지막 충전시작일시
    lastTedt       : 마지막 충전종료일시
    nowTsdt        : 충전중 시작일시
    powerType    : 충전
    output        : 충전용량
    method        : 충전방식
    zcode         : 지역코드
    zscode         : 지역구분 상세코드
    kind           : 충전소 구분코드
    kindDetail     : 충전소 구분 상세코드
    parkingFree    : 주차료무료(y/n)
    note           : 충전소 안내   
    limitYn        : 이용자 제한
    limitDetail    : 이용제한 사유 
    delYn          : 삭제 여부(최근삭제된 충전기 정보 제공(y/n))
    delDetail      : 삭제 사유
    trafficYn      : 편의제공 여부(y/n)
    year           : 설치년도
    floorNum       : 지상/지하 층수
    floorType      : 지상/지하 구분  

"""

"""
class ChargerStatDto:
    busiId       : 기관아이디
    statId   :충전소ID
    chgerId   :충전기ID
    stat   :충전기상태(1: 통신이상, 2:충전대기, 3:충전중, 4:운영중지, 5:점검중, 9:상태미확인)
    statUpdDt   :상태갱신일시
    lastTsdt   :마지막 충전시작 일시
    lastTedt   :마지막 충전종료 일시
    nowTsdt   :충전중 시작일시
"""

# | 코드     | 충전 방식                    | 전력(kW) 예시          | 60kWh 완충 시간                   |
# | ------ | ------------------------ | ------------------ | ----------------------------- |
# | **01** | DC 차데모                   | 50kW               | **약 1시간~1.5시간**               |
# | **03** | DC 차데모 + AC3상            | DC50kW             | **약 1시간~1.5시간**               |
# | **04** | DC 콤보 (CCS1)             | 50~350kW           | **20분~1.5시간**                 |
# | **05** | DC 차데모 + DC 콤보           | 50kW 이상            | **약 1시간~1.5시간**               |
# | **06** | DC 차데모 + AC3상 + DC 콤보    | 최대 50~350kW        | **20분~1.5시간**                 |
# | **08** | DC 콤보(완속) → 실질적으로 7kW 수준 | 7kW                | **약 8~10시간**                  |
# | **09** | NACS(테슬라)                | 150~250kW(슈퍼차저 기준) | **20~40분**                    |
# | **10** | DC 콤보 + NACS             | 150~350kW          | **20~40분**                    |
# | **11** | DC 콤보2(버스용)              | 200~450kW          | **15~30분** (대형 배터리 기준은 1~2시간) |

# | 코드     | 충전 방식 | 전력(kW) 예시 | 60kWh 완충 시간 |
# | ------ | ----- | --------- | ----------- |
# | **02** | AC 완속 | 7kW       | **8~10시간**  |
# | **07** | AC 3상 | 11~22kW   | **3~6시간**   |

