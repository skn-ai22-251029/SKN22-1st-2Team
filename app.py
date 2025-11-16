# ----------------------------- 전체 코드 (팝업 없이, 툴팁 유지 + ETA 시간 표시) -----------------------------
# 스트림릿
from dataclasses import asdict
import streamlit as st
import layout

# 지도
from streamlit_folium import st_folium
import folium

# 현위치
from streamlit_js_eval import get_geolocation

# 스케줄러(옵션)
import threading
import time
import schedule

# 시간 계산 (추가)
from datetime import datetime, timedelta, timezone
from services.charger_detail.select_charger_detail_by_charger_id import (
    select_charger_detail_by_charger_id,
)

KST = timezone(timedelta(hours=9))
def expected_time_from_now_tsdt(status):
    """
    - charger_type in ('01', '03', '04', '05', '09', '10', '11') and now_tsdt -> now_tsdt + 30분
    - charger_type in ('02', '07', '08') and now_tsdt -> now_tsdt + 4시간
    - else -> None
    반환은 KST 기준의 timezone-aware datetime
    """
    base = status.now_tsdt
    if base is None:
        return None
    # naive datetime이면 KST로 간주
    if base.tzinfo is None:
        base = base.replace(tzinfo=KST)
    else:
        base = base.astimezone(KST)

    if status.charger_type in ('01', '03', '04', '05', '09', '10', '11'):
        return base + timedelta(minutes=30)
    elif status.charger_type in ('02', '07', '08'):
        return base + timedelta(hours=4)
    else:
        return None

# 서비스
from services.charger_status import select_charger_status
from services.charger_station.select_charger_station import (
    select_charger_station,
    select_charger_station_location,
)
from services.scheduler import job
from data.data_set import get_all_data_to_excel  # 다운로드 버튼용
from services.price import select_charge_price

from services.charger_detail.select_charger_detail import select_charger_detail
# --------------------------------------------------------------------
# 기본 레이아웃
layout.base_layout()
st.title("EV 충전소 모니터링")

# 지도/정보 2컬럼 레이아웃
left, right = st.columns([3, 2])

# 세션 상태 준비 (선택된 충전소 유지)
if "selected_station" not in st.session_state:
    st.session_state["selected_station"] = None

# --------------------- 위치 좌표 가져오기 ---------------------
loc = get_geolocation()
MY_LAT, MY_LNG = 0.0, 0.0
if loc:
    try:
        MY_LAT = float(loc["coords"]["latitude"])
        MY_LNG = float(loc["coords"]["longitude"])
    except Exception:
        pass

# --------------------- 지도 렌더링 ---------------------
with left:
    if loc:
        # 지도 생성
        m = folium.Map(location=[MY_LAT, MY_LNG], zoom_start=13)

        # 내 위치 마커
        folium.Marker(
            [MY_LAT, MY_LNG],
            tooltip="📍 현재 위치",
            icon=folium.Icon(color="red", icon="user"),
        ).add_to(m)

        # 주변 충전소 조회 & 마커 표시
        datas = select_charger_station_location(MY_LAT, MY_LNG)
        charger_data = [asdict(d) for d in (datas or [])]

        # 좌표 → station_id 매핑 (반올림 키)
        def key_latlng(lat, lng):
            return (round(float(lat), 6), round(float(lng), 6))

        id_by_latlng = {
            key_latlng(c["lat"], c["lng"]): c["station_id"]
            for c in charger_data
        }

        # 마커: 팝업 없이(=말풍선 없음), 툴팁만 유지
        for c in charger_data:
            folium.Marker(
                [c["lat"], c["lng"]],
                # popup=c["station_id"],           # ❌ 제거: 팝업(말풍선) 표시 안 함
                tooltip=f"🔋 {c.get('station_name','')}",  # ✅ 툴팁 유지
                icon=folium.Icon(color="blue", icon="bolt"),
            ).add_to(m)

        # Folium 지도 출력
        st_data = st_folium(m, height=520)

        # --------------------- 클릭 이벤트 처리 (좌표로 station_id 복원) ---------------------
        if st_data:
            station_id = None

            clicked = st_data.get("last_object_clicked")
            if clicked:
                lat = float(clicked.get("lat"))
                lng = float(clicked.get("lng"))

                # 1차: 반올림 키로 매칭
                station_id = id_by_latlng.get(key_latlng(lat, lng))

                # 2차: 근접 탐색(하버사인, 허용 오차 25m)
                if station_id is None and charger_data:
                    from math import radians, sin, cos, sqrt, atan2
                    def haversine(lat1, lon1, lat2, lon2):
                        R = 6371000.0  # meters
                        p1, p2 = radians(lat1), radians(lat2)
                        dphi = radians(lat2 - lat1)
                        dlmb = radians(lon2 - lon1)
                        a = sin(dphi/2)**2 + cos(p1)*cos(p2)*sin(dlmb/2)**2
                        return 2*R*atan2(sqrt(a), sqrt(1-a))

                    nearest = min(
                        charger_data,
                        key=lambda c: haversine(lat, lng, float(c["lat"]), float(c["lng"]))
                    )
                    dist_m = haversine(lat, lng, float(nearest["lat"]), float(nearest["lng"]))
                    if dist_m <= 25:  # 허용 오차
                        station_id = nearest["station_id"]

            if station_id:
                rows = [asdict(d) for d in select_charger_station(station_id) or []]
                if rows:
                    st.session_state["selected_station"] = rows[0]
    else:
        st.warning("📍 위치 권한을 허용해 주세요. (브라우저 팝업 확인)")

# --------------------- 오른쪽 상세 패널 ---------------------
with right:
    data = st.session_state.get("selected_station")
    if data is None:
        st.info("지도 마커를 눌러주세요")
    else:
        # 필요한 컬럼들 안전하게 추출
        station_name = data.get("station_name", "-")
        use_time     = data.get("use_time", "-")
        addr         = data.get("addr", "")
        location_txt = data.get("location", "")
        limit_detail = data.get("limit_detail") or "-"
        station_id   = data.get("station_id")
        operator_id  = data.get("operator_id")
        parking_free = data.get("parking_free")
        floor_num = data.get("floor_num")
        floor_type = data.get("floor_type")

        # 충전 가격 조회 → 급속/완속 가격 채우기
        rapid_price = 300
        slow_price  = 280
        try:
            prices = select_charge_price.select_charger_price(operator_id)
            for price in prices or []:
                # 01: 급속, 02: 완속 (프로젝트 정의에 맞게 사용)
                if price.price_type_code == '01':
                    rapid_price = float(price.guest_price)
                elif price.price_type_code == '02':
                    slow_price = float(price.guest_price)
        except Exception:
            pass
        
        # 주차비 무료/유료
        if parking_free == 'Y':
            parking_free = '무료'
        else:
            parking_free = '유료'
        
        # 지상/지하
        if floor_type == 'F':
            floor_type = '지상'
        else:
            floor_type = '지하'

        # 가격 기반 파생값 계산
        eta_rapid = int(rapid_price) * 50
        eta_slow  = int(slow_price)  * 7 * 4

        # --- 카드형 출력(간단) ---
        st.markdown("### ⛽ 충전소 정보")
        st.write(f"**충전소** : {station_name}, {floor_type} {floor_num}층")
        
        st.write("")  # 여백
        rp_txt = f"{rapid_price:,.0f}원"
        sp_txt = f"{slow_price:,.0f}원"
        st.write(f"**충전 요금** : 급속 {rp_txt} / 완속 {sp_txt}")
        st.write(f"**주차비** : {parking_free}")
        st.write(f"**예상 완충 비용** : 급속 {eta_rapid:,.0f}원 / 완속 {eta_slow:,.0f}원")

        st.write("")  # 여백
        st.write(f"**주소** : {addr} {location_txt}")
        if use_time in ('~','0000~0000'):
            use_time = '24시간 이용가능'
        st.write(f"**이용 시간** : {use_time}")
        st.write(f"**제한** : {limit_detail}")

        st.write("")  

        # 충전기 상태 표시 (charger_status 기반, charger_detail과 매칭하여 ETA 계산)
        charger_status_list = select_charger_status.select_charger_status(station_id)
        if charger_status_list:
            st.write(f"** 충전기 현황 **")
            st.write(f'전체 충전기 수: {len(charger_status_list)}')

            for num, charger_status_obj in enumerate(charger_status_list):
                # 1:통신이상,2:대기,3:충전중,4:운영중지,5:점검중,9:미확인
                info = None
                if charger_status_obj.stat == 2:
                    info = '현재 충전 대기중입니다.'
                elif charger_status_obj.stat == 3:
                    info = '현재 충전중입니다.'
                elif charger_status_obj.stat == 4:
                    info = '현재 운영중지 입니다.'
                elif charger_status_obj.stat == 5:
                    info = '현재 점검중입니다.'
                elif charger_status_obj.stat == 9:
                    info = '미확인 상태입니다.'

                st.write(f'{num+1}번째 충전기 : {info}')

                # ETA 계산 로직
                # stat == 2 (대기): "현재" 출력
                # stat == 3 (충전중): now_tsdt가 있으면 시간 계산해서 출력
                # stat == 4,5,9 (정지/점검/미확인): "예상 시간 정보 없음"
                
                if charger_status_obj.stat == 2:
                    # 대기 상태 → "현재 충전 가능"
                    eta_str = "예상 이용 가능 시간 : 현재"
                elif charger_status_obj.stat == 3:
                    # 충전중 → now_tsdt로 계산
                    charger_id = getattr(charger_status_obj, 'charger_id', '')
                    detail = None
                    try:
                        detail = select_charger_detail_by_charger_id(charger_id)
                    except Exception:
                        detail = None

                    eta_str = "예상 시간 정보 없음"
                    # detail 또는 charger_status_obj에서 now_tsdt 찾기
                    now_tsdt = None
                    if detail and hasattr(detail, 'now_tsdt'):
                        now_tsdt = detail.now_tsdt
                    elif hasattr(charger_status_obj, 'now_tsdt'):
                        now_tsdt = charger_status_obj.now_tsdt

                    # now_tsdt가 있으면 ETA 계산
                    if now_tsdt:
                        try:
                            # 임시 객체 생성해서 expected_time_from_now_tsdt에 전달
                            class TempObj:
                                def __init__(self, now_tsdt_val, charger_type_val):
                                    self.now_tsdt = now_tsdt_val
                                    self.charger_type = charger_type_val

                            charger_type = detail.charger_type if detail else '02'
                            temp = TempObj(now_tsdt, charger_type)
                            eta = expected_time_from_now_tsdt(temp)
                            if eta is not None:
                                eta_str = f"예상 이용 가능 시각 : {eta.strftime('%Y-%m-%d %H:%M')}"
                        except Exception:
                            pass
                else:
                    # 운영중지, 점검중, 미확인 등
                    eta_str = "예상 시간 정보 없음"

                st.write(eta_str)

# --------------------- 스케줄러 (옵션) ---------------------
# schedule.every(30).minutes.do(job)

def background_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

if "scheduler_started" not in st.session_state:
    threading.Thread(target=background_thread, daemon=True).start()
    st.session_state["scheduler_started"] = True
    st.caption("⏱️ 백그라운드 스케줄러 동작 중 (필요 시 schedule 주석 해제)")

st.write("---")

# --------------------- 수동 실행 / 전체 데이터 다운로드 ---------------------
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("수동 실행"):
        job()
        st.success("수동으로 job() 실행 완료!")

with col_btn2:
    if st.button("전체 데이터 다운로드"):
        get_all_data_to_excel()
        st.success("ev_charger_data.xlsx 저장 완료 (앱이 실행되는 서버/로컬 경로)")
# --------------------------------------------------------------------
