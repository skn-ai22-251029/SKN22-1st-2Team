from dataclasses import dataclass
from typing import Optional

@dataclass
class ChargerInfoDTo:
    statNm         : Optional[str]=None                 
    statId        : Optional[str]=None
    chgerId       : Optional[str]=None
    chgerType     : Optional[str]=None
    addr          : Optional[str]=None
    addrDetail     : Optional[str]=None                
    lat            : Optional[str]=None
    lng            : Optional[str]=None
    useTime        : Optional[str]=None 
    busiId        : Optional[str]=None
    bnm            : Optional[str]=None
    busiNm         : Optional[str]=None
    busiCall       : Optional[str]=None
    stat          : Optional[str]=None
    statUpdDt      : Optional[str]=None
    lastTsdt       : Optional[str]=None
    lastTedt       : Optional[str]=None
    nowTsdt        : Optional[str]=None
    powerType    : Optional[str]=None
    output        : Optional[str]=None
    method        : Optional[str]=None
    zcode         : Optional[str]=None
    zscode         : Optional[str]=None
    kind           : Optional[str]=None
    kindDetail     : Optional[str]=None
    parkingFree    : Optional[str]=None    
    note           : Optional[str]=None   
    limitYn        : Optional[str]=None
    limitDetail    : Optional[str]=None 
    delYn          : Optional[str]=None
    delDetail      : Optional[str]=None 
    trafficYn      : Optional[str]=None 
    year           : Optional[str]=None
    floorNum       : Optional[str]=None
    floorType      : Optional[str]=None   


