# SKN22-1st-2Team
Repository for SKN22-1st-2Team

## ✅ Dev Environment
- **Python**: 3.13.9
- **Conda env**: `grilled_kim`
  - install pakage
    - pyyaml
    - requests
- **Database**: MySQL (스키마 및 테이블 구성은 `/repository/schema.sql` 참고 예정)

---

# 🚗 전기차 충전소 통합 정보 시스템

> 공공데이터 Open API 기반으로 전국 전기차 충전소 정보를 통합하여  
> 검색 · 지도 시각화 · 요금 비교 · 경로 추천 등 주요 기능을 제공하는 웹 서비스입니다.

---

## 📌 주요 기능 요약

### ✅ 1. 충전소 검색 기능
- 주소/지역 기반으로 충전소 목록 조회
- 시·도/시·군·구 필터링
- 지역별 충전소 개수, 급속/완속 비율 시각화 차트 제공

### ✅ 2. 지도 기반 시각화 + 주변 편의시설
- 위도·경도 기반 지도 마커 표시(PyDeck/Streamlit Map)
- 충전소 위치 시각적 확인 및 주변 시설 정보 연계 가능(추가 개발 여지)

### ✅ 3. 충전소 상세 정보 조회
- 충전기 타입(급속/완속) 및 수량 정보 표시
- 요금 정보 및 운영사 정보
- 현재 충전 여부 및 예상 대기시간 계산

### ✅ 4. 요금 비교 기능
- 사업자별 평균 요금 비교
- 급속/완속별 평균 요금 비교 시각화

### ✅ 5. 경로 기반 추천
- 출발지 → 도착지 경로 상 충전소 자동 추천
- 지도 기반 경로 위 충전소 필터링

---

# 🧠 시스템 아키텍처

                  ┌──────────────────────────────────────┐
                  │           공공데이터 Open API         │
                  │     (전기차 충전소·상세·상태 정보)     │
                  └───────────────────┬───────────────────┘
                                      │  JSON 응답
                                      ▼
                         ┌──────────────────────────┐
                         │  services/api/get_charger_data.py │
                         │   • API 호출 및 예외 처리          │
                         │   • 데이터 정제 / 구조화           │
                         └───────────────┬───────────────────┘
                                         │ 정제된 데이터
                                         ▼
                        ┌────────────────────────────────────┐
                        │         MySQL : ev_charger_db       │
                        │  • charger_station / detail / status │
                        │  • charge_price                     │
                        └──────────────┬──────────────────────┘
                                       │ SQL Insert / Select
                                       ▼
     ┌──────────────────────────────┬───────────────────────────────────┬──────────────────────────────┐
     │                              │                                   │                              │
┌──────────────────────┐  ┌──────────────────────────┐   ┌────────────────────────┐      ┌─────────────────────────┐
│ repository/db.py      │  │ services/*_insert_.py    │   │ services/*_select_.py   │      │  services/price/*.py      │
│ • DB Connection Pool  │  │ • 저장/업데이트 처리      │   │ • 조회/필터링/검색 로직     │      │ • 요금 스크래핑 및 정제        │
└──────────────────────┘  └──────────────────────────┘   └────────────────────────┘      └─────────────────────────┘
               │                         │                         │                               │
               └─────────────────────────┴───────────────┬─────────┴──────────────────────────────┘
                                                         ▼
                                 ┌────────────────────────────────────────────┐
                                 │               DTO Layer                    │
                                 │  charger_info / price / stat DTO          │
                                 │  • UI/서비스 간 데이터 전송 전용 구조        │
                                 └──────────────────────────┬─────────────────┘
                                                            │ 전달
                                                            ▼
                           ┌────────────────────────────────────────────────────────────────────┐
                           │                             Streamlit UI                           │
                           │               app.py  +  pages/*.py (검색/지도/상세/요금/FAQ)         │
                           │               • 지도 시각화 (Folium)                               │
                           │               • 상태 업데이트 모니터링                              │
                           │               • 검색/필터/마커 UI                                   │
                           └────────────────────────────────────────────────────────────────────┘


📦 프로젝트 구조

├── 📄 app.py  
├── 📄 layout.py  
│
├── 📁 services/                         💬 주요 비즈니스 로직 및 데이터 처리 계층
│   ├──📄scheduler.py                             💬 배치, 스케줄러, 크롤러 실행 스크립트
│   ├── 📁 api/
│   │   └── 📄 get_charger_data.py          💬 공공데이터 API 연동 클라이언트
│   │
│   ├── 📁 charger_station/
│   │   ├── 📄 insert_charger_station.py     💬 충전소 정보 등록 및 중복 처리 로직
│   │   └── 📄 select_charger_station.py     💬 충전소 조회 로직
│   │
│   ├── 📁 charger_detail/
│   │   ├── 📄 insert_charger_detail.py      💬 세부 충전기 정보 저장
│   │   └── 📄 select_charger_detail.py      💬 세부 충전기 조회
│   │
│   ├── 📁 charger_status/
│   │   ├── 📄 insert_charger_status.py      💬 충전기 상태 정보 업데이트
│   │   └── 📄 select_charger_status.py      💬 상태 조회 및 모니터링
│   │
│   ├── 📁 price/
│   │   ├── 📄 get_charge_price.py           💬 스크래핑 또는 API 기반 요금 수집
│   │   ├── 📄 insert_charge_price.py        💬 요금 데이터 저장
│   │   └── 📄 select_charge_price.py        💬 요금 데이터 조회
│   │
│   └── 📁 repository/
│       └── 📄 db.py                         💬 MySQL 연결 및 커넥션 팩토리
│
├── 📁 DTO/                              💬 데이터 전송 객체 (입출력 전용)
│   ├── 📄 charger_info_dto.py
│   ├── 📄 charger_price_dto.py
│   └── 📄 charger_stat_dto.py
│
├── 📁 models/                           💬 Domain Model (엔티티 클래스)
│   ├── 📄 charger_station.py
│   ├── 📄 charger_detail.py
│   ├── 📄 charger_status.py
│   └── 📄 charger_price.py
│
├── 📁 data/                             💬 정적 데이터 및 엑셀/CSV 저장용 폴더
│   └── 📄 data_set.py                      💬 API 수집 데이터를 엑셀로 변환/다운로드
│   
│
└── 📁 scripts/                          💬 배치, 스케줄러, 크롤러 실행 스크립트
    ├── 📄 create_database.sql         💬 db생성 및 권한 처리
    └── 📄 create_table.sql              💬 데이터 테이블 생성 

<img width="1900" height="2140" alt="Untitled diagram-2025-11-16-132038" src="https://github.com/user-attachments/assets/6a39534d-ebb9-48ca-b56d-1cec09c198d2" />


