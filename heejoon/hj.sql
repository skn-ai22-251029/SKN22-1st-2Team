select
    
from
    charger_station A join charger_status B
        on A.station_id = B.station_id join charger_detail C
            on B.charger_id = C.charger_id join charger_meta D
                on C.charger_type = D.charger_type
where
    case 
        when D.charger_type = '01' then;

select
    description
from
    charger_meta
where
    charger_type in ('01','02','03','04','05','06','07','08','09','10','11');

