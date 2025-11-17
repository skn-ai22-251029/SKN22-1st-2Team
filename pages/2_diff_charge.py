import streamlit as st
import pandas as pd
from services.price.select_charge_price import select_price_by_region
from services.charger_station.select_charger_station import select_available_regions

import layout

layout.base_layout()

st.title("💾요금 비교 페이지")

# ===== 지역별 요금 비교 =====
st.subheader("지역을 선택하여 요금을 비교하세요")

# 모든 충전소에서 지역 추출 (area_code_master에 정의된 지역만 사용)
regions = select_available_regions() or []

if regions:
    regions_code, regions_name = zip(*regions)

    selected_region = st.selectbox(
        "지역 선택",
        options=regions_name,
        key="region_select"
    )
    print("-" * 100)
    print(selected_region)
    if selected_region:
        # 선택 지역의 요금 조회 (busi_id 기준 매칭)
        region_prices = select_price_by_region(selected_region)
        
        if region_prices:
            # 최저가 비교 (먼저 표시)
            st.write("💰 **최저가 비교**")
            
            # 급속 최저가
            rapid_prices = []
            for operator, prices in region_prices.items():
                for p in prices:
                    if p.price_type_code == '01' and p.guest_price:
                        try:
                            rapid_prices.append((operator, p.guest_price))
                        except:
                            pass
            
            if rapid_prices:
                min_rapid = min(rapid_prices, key=lambda x: x[1])
                st.success(f"🔋 **급속 충전 최저가**: {min_rapid[0]} - {min_rapid[1]}원")
            
            # 완속 최저가
            slow_prices = []
            for operator, prices in region_prices.items():
                for p in prices:
                    if p.price_type_code == '02' and p.guest_price:
                        try:
                            slow_prices.append((operator, p.guest_price))
                        except:
                            pass
            
            if slow_prices:
                min_slow = min(slow_prices, key=lambda x: x[1])
                st.success(f"⚙️ **완속 충전 최저가**: {min_slow[0]} - {min_slow[1]}원")
            
            # 요금 비교 표 (아래에 표시)
            st.write("---")
            st.write(f"**{selected_region} 지역의 충전 요금**")
            
            # 각 운영기관별로 표시
            for operator_name, prices in sorted(region_prices.items()):
                with st.expander(f"📍 {operator_name}"):
                    price_data = []
                    for price in prices:
                        price_data.append({
                            "충전 유형": price.price_type_name,
                            "비회원 요금": f"{price.guest_price}원" if price.guest_price else "-",
                            "회원 요금": f"{price.member_price}원" if price.member_price else "-",
                            "업데이트": price.update_dt
                        })
                    
                    df = pd.DataFrame(price_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning(f"{selected_region} 지역의 요금 정보가 없습니다.")
else:
    st.warning("지역 정보를 불러올 수 없습니다.")