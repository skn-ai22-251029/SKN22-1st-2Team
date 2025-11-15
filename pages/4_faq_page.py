from services.faq import faq
import streamlit as st
import layout
import math
import re
from html import escape

layout.base_layout()

# 질문/답변 리스트
question_lst=faq.question_lst

# Helpers

ITEMS_PER_PAGE = 5

def _terms_from_query(q: str):
    q = (q or "").strip()
    if not q:
        return []
    # 공백 기준 분리, 한글/영문 혼합 단어도 포함
    terms = [t for t in re.split(r"\s+", q) if t]
    # 길이 1짜리 단어도 허용(요청사항: 포함된 단어는 노란색 처리)
    return terms

def highlight(text: str, terms):
    if not terms:
        return escape(text)
    pattern = r"(" + "|".join(re.escape(t) for t in terms) + r")"
    def repl(m):
        return f"<mark>{escape(m.group(0))}</mark>"
    # 먼저 escape로 안전 처리 후, 매칭 구간만 다시 덮어쓰기 위해 raw에서 처리
    # (간단화를 위해 여기서는 원문에 직접 적용)
    return re.sub(pattern, repl, text, flags=re.IGNORECASE)


# Title & Controls

st.title("❓ FAQ - 자주 묻는 질문")

# 검색어 입력
q = st.text_input("검색어", placeholder="키워드로 검색 (예: 요금, 경로, 위치)")
terms = _terms_from_query(q)

# 페이지 상태 초기화/관리 (검색어가 바뀌면 1페이지로)
if "faq_page" not in st.session_state:
    st.session_state.faq_page = 1
if "_last_query" not in st.session_state:
    st.session_state._last_query = ""
if q != st.session_state._last_query:
    st.session_state.faq_page = 1
    st.session_state._last_query = q


# Filter

filtered = []
query_lower = (q or "").strip().lower()
for question, answer in question_lst:
    if not query_lower:
        filtered.append((question, answer))
    else:
        if (query_lower in question.lower()) or (query_lower in answer.lower()):
            filtered.append((question, answer))

# 페이지 수 계산 및 범위 보정
total_pages = max(1, math.ceil(len(filtered) / ITEMS_PER_PAGE))
page = max(1, min(st.session_state.faq_page, total_pages))

start_idx = (page - 1) * ITEMS_PER_PAGE
end_idx = start_idx + ITEMS_PER_PAGE
paged = filtered[start_idx:end_idx]

st.caption(f"총 {len(filtered)}개 결과 · 페이지 {page}/{total_pages}")


# Render

if not paged:
    st.info("검색 조건에 맞는 FAQ가 없습니다. 키워드를 조정해 보세요.")
else:
    for i, (question, answer) in enumerate(paged, start=start_idx + 1):
        with st.expander(f"Q{i}. {question}"):
            # 제목과 본문에서 검색어 하이라이트
            st.markdown(f"**Q{i}.** " + highlight(question, terms), unsafe_allow_html=True)
            st.markdown(highlight(answer, terms), unsafe_allow_html=True)

# -----------------------------
# Pagination 
# -----------------------------
left, mid, right = st.columns([1, 6, 1])
with left:
    if st.button("⬅ 이전 페이지", use_container_width=True, disabled=(page <= 1)):
        st.session_state.faq_page = max(1, page - 1)
with right:
    if st.button("다음 페이지 ➡", use_container_width=True, disabled=(page >= total_pages)):
        st.session_state.faq_page = min(total_pages, page + 1)