from dataclasses import dataclass
from typing import Optional

class ChargerStatDto:
    busiId       :Optional[str]=None
    statId   :Optional[str]=None
    chgerId   :Optional[str]=None
    stat   :Optional[str]=None
    statUpdDt   :Optional[str]=None
    lastTsdt   :Optional[str]=None
    lastTedt   :Optional[str]=None
    nowTsdt   :Optional[str]=None
