select
    C.region '지역명',
    B.station_id '충전소 번호',
    A.member_price '멤버 적용가',
    
    A.guest_price '일반고객 적용가'
   
from
    charge_price A join charger_station B
        on A.operator_code = B.operator_id join area_code_master C
            on B.zscode = C.zscode

group by
   C.zscode;