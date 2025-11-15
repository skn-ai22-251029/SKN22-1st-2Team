# 스트림릿
import streamlit as st
import layout

# 지도, 그래프
import pandas as pd
from streamlit_folium import st_folium
import folium

# 현위치
from streamlit_js_eval import get_geolocation

# 스케줄러
import threading
import time
import schedule
from services.charger_station.select_charger_station import select_charger_station
from services.scheduler import job

layout.base_layout()

# 현 위치 가져오기
loc = get_geolocation()

if loc:
    # 지도 변수/상수
    MY_LAT = float(loc["coords"]["latitude"])
    MY_LON = float(loc["coords"]["longitude"])

    # Folium 지도 객체 생성
    m = folium.Map(location=[MY_LAT, MY_LON], zoom_start=13)

    # 내 위치 마커
    folium.Marker(
        [MY_LAT, MY_LON],
        popup="📍 내 위치",
        tooltip="현재 위치",
        icon=folium.Icon(color="red", icon="user"),
    ).add_to(m)

    datas = select_charger_station()

    charger_data = [
        {"name": d.station_name, "lat": d.lat, "lng": d.lng}
        for d in datas or []
    ]

    # 충전소 마커 표시
    for c in charger_data:
        folium.Marker(
            [c["lat"], c["lng"]],
            popup=f"🔋 {c['name']}<br>상세보기 클릭!",
            tooltip=c["name"],
            icon=folium.Icon(color="blue", icon="bolt"),
        ).add_to(m)

    # ---- Folium 지도 렌더링 ----
    st_data = st_folium(m, width=800, height=600)

    # ---- 클릭 이벤트 ----
    if st_data and st_data["last_clicked"]:
        lat = st_data["last_clicked"]["lat"]
        lon = st_data["last_clicked"]["lng"]
        st.success(f"🖱️ 클릭한 위치: ({lat:.6f}, {lon:.6f})")
        # 예: DB나 API를 이용한 충전소 상세조회
        st.write(
            "👉 이 좌표 인근의 충전소 정보를 불러오는 로직을 여기에 추가할 수 있습니다."
        )
else:
    st.warning("📍 위치 정보를 불러오는 중이거나, 권한이 거부되었습니다.")

# 스케줄 등록
schedule.every(30).minutes.do(job)


def background_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


if "scheduler_started" not in st.session_state:
    threading.Thread(target=background_thread, daemon=True).start()
    st.session_state["scheduler_started"] = True
    st.success("백그라운드 스케줄러 시작됨")

st.title("EV 충전소 모니터링")
st.write("스케줄러가 30분마다 자동 실행 중입니다.")
if st.button("수동 실행"):
    job()
    st.info("수동으로 job() 실행 완료!")
