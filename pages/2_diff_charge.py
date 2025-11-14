import streamlit as st
import layout
from services.get_charge_price import scrapping_charge_price

layout.base_layout()

st.write('요금 비교 페이지')
if st.button('정보 가져오기!'):
    scrapping_charge_price()
    print('요금정보 등록 완료')