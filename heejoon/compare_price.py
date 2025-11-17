import traceback
from models import charger_station
from models.charger_detail import Charger_detail
from models.charger_station import Charger_station
from models.charger_status import Charger_status
from models.charge_price import ChargePrice
from repository.db import get_connection


def compare_price():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            select

            from
                charger_station A join charger_station B
                    on B.operator_code = A.operator_id join area_code_master C
                        on C.zcode = 

"""

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

# language: python
import streamlit as st
import pandas as pd
from typing import Union, List, Dict

def show_ev_fee_comparison(
    data: Union[pd.DataFrame, List[Dict]],
    title: str = "지역별 전기차 충전 요금 비교표",
    region_col: str = "지역",
    highlight_min: bool = True,
    currency: str = "원"
):
    """
    Streamlit에 지역별 전기차 충전 요금 비교표를 표시.
    - data: DataFrame 또는 list[dict]. 각 행에 '지역'과 요금(숫자) 컬럼들 필요.
    - region_col: 지역명을 담은 컬럼명(기본 '지역').
    - highlight_min: 컬럼별 최저값 배경색 표시 여부.
    - currency: 통화 표시(기본 '원').
    """
    # DataFrame 변환
    df = pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data.copy()
    if region_col not in df.columns:
        st.error(f"'{region_col}' 컬럼이 데이터에 없습니다.")
        return

    # 숫자 컬럼(지역 컬럼 제외)
    value_cols = [c for c in df.columns if c != region_col]
    # 숫자 변환
    df[value_cols] = df[value_cols].apply(pd.to_numeric, errors="coerce")

    st.header(title)

    if highlight_min and value_cols:
        # 스타일: 컬럼별 최저값 배경색 표시
        def _highlight_min(col):
            is_min = col == col.min()
            return ["background-color: #d4f7d4" if v else "" for v in is_min]

        fmt = {c: "{:,.0f} " + currency for c in value_cols}
        styled = df.style.format(fmt).apply(_highlight_min, subset=value_cols)
        st.dataframe(styled)  # Streamlit은 pandas Styler 지원
    else:
        st.table(df)

    # 항목별 최저값 요약
    if value_cols:
        st.subheader("항목별 최저 요금")
        for c in value_cols:
            if df[c].dropna().empty:
                st.write(f"- {c}: 데이터 없음")
                continue
            idx = df[c].idxmin()
            region = df.at[idx, region_col]
            value = df.at[idx, c]
            st.write(f"- {c}: {region} — {value:,.0f} {currency}")