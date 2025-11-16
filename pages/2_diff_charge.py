import streamlit as st
import layout
from services.price.get_charge_price import scrapping_charge_price
from services.price.select_charge_price import (
    select_all_charger_price,
    select_price_by_region,
    select_price_by_station,
)
from services.charger_station.select_charger_station import select_all_charger_station
import pandas as pd

layout.base_layout()

st.title("💾요금 비교 페이지")

# 요금 정보 새로고침 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button('💾 요금 정보 새로고침'):
        try:
            scrapping_charge_price()
            st.success('요금정보 업데이트 완료!')
        except Exception as e:
            st.error(f'요금정보 업데이트 실패: {e}')

# 탭 구성
tab1, tab2 = st.tabs(["지역별 요금 비교", "충전소별 요금 비교"])

# ===== TAB 1: 지역별 요금 비교 =====
with tab1:
    st.subheader("지역을 선택하여 요금을 비교하세요")
    
    # 모든 충전소에서 지역 추출
    all_stations = select_all_charger_station() or []
    regions = set()
    
    for station in all_stations:
        addr = getattr(station, 'addr', '')
        if addr:
            region = addr.split()[0]  # 첫 번째 단어 (시도)
            regions.add(region)
    
    regions = sorted(list(regions))
    
    if regions:
        selected_region = st.selectbox(
            "지역 선택",
            options=regions,
            key="region_select"
        )
        
        if selected_region:
            # 선택 지역의 요금 조회 (busi_id 기준 매칭)
            region_prices = select_price_by_region(selected_region)
            
            if region_prices:
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
                
                # 최저가 비교
                st.write("---")
                st.write("💰 **최저가 비교**")
                
                # 급속 최저가
                rapid_prices = []
                for operator, prices in region_prices.items():
                    for p in prices:
                        if p.price_type_code == '01' and p.guest_price:
                            try:
                                rapid_prices.append((operator, float(p.guest_price), p))
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
                                slow_prices.append((operator, float(p.guest_price), p))
                            except:
                                pass
                
                if slow_prices:
                    min_slow = min(slow_prices, key=lambda x: x[1])
                    st.success(f"⚙️ **완속 충전 최저가**: {min_slow[0]} - {min_slow[1]}원")
            else:
                st.warning(f"{selected_region} 지역의 요금 정보가 없습니다.")
    else:
        st.warning("지역 정보를 불러올 수 없습니다.")


# ===== TAB 2: 충전소별 요금 비교 =====
with tab2:
    st.subheader("충전소를 선택하여 요금을 확인하세요")
    
    all_stations = select_all_charger_station() or []
    
    if all_stations:
        # 충전소 목록 생성
        station_options = {}
        for s in all_stations:
            station_id = getattr(s, 'station_id', '')
            station_name = getattr(s, 'station_name', 'N/A')
            addr = getattr(s, 'addr', 'N/A')[:30]
            display_name = f"{station_name} ({addr})"
            station_options[display_name] = station_id
        
        selected_station_name = st.selectbox(
            "충전소 선택",
            options=list(station_options.keys()),
            key="station_select"
        )
        
        if selected_station_name:
            station_id = station_options[selected_station_name]
            
            # 해당 충전소의 요금 조회 (busi_id 기준 매칭)
            station_prices = select_price_by_station(station_id)
            
            if station_prices:
                st.write(f"**{selected_station_name}의 충전 요금**")
                
                price_data = []
                for price in station_prices:
                    price_data.append({
                        "운영기관": price.operator_name,
                        "충전 유형": price.price_type_name,
                        "비회원 요금": f"{price.guest_price}원" if price.guest_price else "-",
                        "회원 요금": f"{price.member_price}원" if price.member_price else "-",
                        "업데이트": price.update_dt
                    })
                
                df = pd.DataFrame(price_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # 요금 상세
                st.write("---")
                col_rapid, col_slow = st.columns(2)
                
                rapid = next((p for p in station_prices if p.price_type_code == '01'), None)
                slow = next((p for p in station_prices if p.price_type_code == '02'), None)
                
                with col_rapid:
                    if rapid and rapid.guest_price:
                        st.metric("🔋 급속 충전", rapid.guest_price + "원")
                    else:
                        st.metric("🔋 급속 충전", "정보 없음")
                
                with col_slow:
                    if slow and slow.guest_price:
                        st.metric("⚙️ 완속 충전", slow.guest_price + "원")
                    else:
                        st.metric("⚙️ 완속 충전", "정보 없음")
            else:
                st.warning("해당 충전소의 요금 정보가 없습니다.")
    else:
        st.warning("충전소 정보를 불러올 수 없습니다.")