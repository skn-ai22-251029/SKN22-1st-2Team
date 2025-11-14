from dataclasses import dataclass
from datetime import date

@dataclass
class ChargePrice:
    operator_name: str          # 운영기관명 (BNM)
    rnum: int                   # 순서 인덱스
    price_type_name: str        # 급속/완속 명칭 (PRICE_TYPE_NM)
    update_dt: date             # 업데이트 날짜
    price_type_code: str        # 급속/완속 코드(01/02)
    member_price: str         # 회원요금
    operator_code: str          # 운영기관 코드 (BID)
    guest_price: str          # 비회원요금

    def as_tuple(self):
            return (
                self.operator_name,
                self.rnum,
                self.price_type_name,
                self.update_dt,
                self.price_type_code,
                self.member_price,
                self.operator_code,
                self.guest_price
            )
    

