.pages.2_diff_charge.py 에는 지역별 요금 비교표를 호출하는 함수를 streamlit에서 볼 수 있게 작성만 하고, 지역별 요금 비교표를 호출하는 함수는 .heejoon.compare_price.py에 만들려고해

# ...existing code...
import streamlit as st
import pandas as pd
from typing import Optional, Union, List, Dict

def show_region_charge_comparison(
    data: Optional[Union[pd.DataFrame, List[Dict]]] = None,
    title: str = "지역별 전기차 충전 요금 비교표",
    region_col: str = "지역",
    currency: str = "원",
    highlight_min: bool = True
):
    """
    Streamlit에 지역별 전기차 충전 요금 비교표를 출력합니다.
    - data: DataFrame 또는 list[dict]. None이면 가능한 DB 함수로 시도하여 로드하고, 실패하면 샘플 데이터를 사용합니다.
    - region_col: 지역명 컬럼명
    """
    # 데이터 로드(인자가 없을 때 가능한 DB 호출 시도)
    if data is None:
        try:
            from scripts.select_database import get_charger_price  # 프로젝트에 맞게 조정
            fetched = get_charger_price()  # 함수가 DataFrame 또는 list[dict] 반환한다고 가정
            data = pd.DataFrame(fetched) if not isinstance(fetched, pd.DataFrame) else fetched
        except Exception:
            # 안전한 샘플 백업 데이터
            data = [
                {"지역": "서울", "급속(원/kWh)": 300, "완속(원/kWh)": 200},
                {"지역": "부산", "급속(원/kWh)": 280, "완속(원/kWh)": 210},
                {"지역": "대구", "급속(원/kWh)": 320, "완속(원/kWh)": 190},
            ]

    # DataFrame 변환 및 전처리
    df = pd.DataFrame(data) if not isinstance(data, pd.DataFrame) else data.copy()
    if region_col not in df.columns:
        st.error(f"데이터에 '{region_col}' 컬럼이 없습니다.")
        return

    value_cols = [c for c in df.columns if c != region_col]
    # 숫자 변환
    df[value_cols] = df[value_cols].apply(pd.to_numeric, errors="coerce")

    st.header(title)

    if value_cols and highlight_min:
        def _highlight_min(col):
            if col.dropna().empty:
                return ['' for _ in col]
            is_min = col == col.min()
            return ["background-color: #d4f7d4" if v else "" for v in is_min]

        fmt = {c: "{:,.0f} " + currency for c in value_cols}
        styled = df.style.format(fmt).apply(_highlight_min, subset=value_cols)
        st.write(styled)  # Styler를 그대로 표시
    else:
        st.dataframe(df)

    # 항목별 최저값 요약
    if value_cols:
        st.subheader("항목별 최저 요금")
        for c in value_cols:
            col_series = df[c].dropna()
            if col_series.empty:
                st.write(f"- {c}: 데이터 없음")
                continue
            idx = col_series.idxmin()
            region = df.at[idx, region_col]
            value = df.at[idx, c]
            st.write(f"- {c}: {region} — {value:,.0f} {currency}")
# ...existing code...

# ...existing code...
import streamlit as st
# 기존 페이지 코드들...
from .heejoon.compare_price import show_region_charge_comparison

def main():
    st.title("지역별 충전 요금 비교")
    # 필요한 경우 DB에서 불러와서 인자로 전달하거나, 인자 없이 호출하면 함수 내부에서 시도합니다.
    show_region_charge_comparison()

if __name__ == "__main__":
    main()
# ...existing code...