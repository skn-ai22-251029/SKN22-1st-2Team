# 스트림릿
import streamlit as st
import layout

# 지도, 그래프
import pandas as pd

# 현위치
from streamlit_js_eval import get_geolocation

# 스케줄러
import threading
import time
import schedule
from services.scheduler import job

layout.base_layout()

loc = get_geolocation()


# 지도 변수/상수
MY_PIN_SIZE = 100
MY_PIN_COLOR = [[255, 0, 0], [255, 0, 0], [255, 0, 0]]
CHARGER_PIN_SIZE = 70
CHARGER_PIN_COLOR = [[255, 255, 0], [255, 255, 0], [255, 255, 0]]

df = pd.DataFrame(
    {
        "latitude": float(loc["coords"]["latitude"]),
        "longitude": float(loc["coords"]["longitude"]),
        "size": MY_PIN_SIZE,
        "color": MY_PIN_COLOR,
    }
)

df2 = pd.DataFrame(
    {
        "latitude": 37.476296,
        "longitude": 126.9583876,
        "size": CHARGER_PIN_SIZE,
        "color": CHARGER_PIN_COLOR,
    }
)


combined_df = pd.concat([df, df2], ignore_index=True)

st.map(
    combined_df, latitude="latitude", longitude="longitude", size="size", color="color"
)

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
