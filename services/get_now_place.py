from streamlit_js_eval import get_geolocation
import streamlit as st

st.title("현재 위치(GPS) 테스트")

loc = get_geolocation()

if loc:
    st.write("위도:", loc['coords']['latitude'])
    st.write("경도:", loc['coords']['longitude'])
else:
    st.write("위치 권한 요청 중...")