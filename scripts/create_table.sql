-- ==========================================
-- 1. 운영기관 정보
-- ==========================================
CREATE TABLE operator_info (
    operator_id      VARCHAR(10) PRIMARY KEY COMMENT '기관 아이디 (busiId)',
    org_name         VARCHAR(50) COMMENT '기관명 (bnm)',
    operator_name    VARCHAR(100) COMMENT '운영기관명 (busiNm)',
    operator_call    VARCHAR(20) COMMENT '운영기관 연락처 (busiCall)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==========================================
-- 2. 지역 코드 마스터
-- ==========================================
CREATE TABLE area_code_master (
    zcode        VARCHAR(5) PRIMARY KEY COMMENT '시도 코드',
    zscode       VARCHAR(10) COMMENT '시군구 코드',
    region       VARCHAR(50) COMMENT '시도명',
    sub_region   VARCHAR(50) COMMENT '시군구명'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ==========================================
-- 3. 충전소 기본 정보
-- ==========================================
CREATE TABLE charger_station (
    station_id      VARCHAR(20) PRIMARY KEY COMMENT '충전소ID (statId)',
    station_name    VARCHAR(100) COMMENT '충전소명 (statNm)',
    addr            VARCHAR(200) COMMENT '주소 (addr)',
    addr_detail     VARCHAR(200) COMMENT '주소상세 (addrDetail)',
    location        VARCHAR(200) COMMENT '상세위치 (location)',
    lat             DOUBLE COMMENT '위도 (lat)',
    lng             DOUBLE COMMENT '경도 (lng)',
    use_time        VARCHAR(50) COMMENT '이용가능시간 (useTime)',
    parking_free    CHAR(1) COMMENT '주차료무료 (parkingFree)',
    note            VARCHAR(200) COMMENT '충전소 안내 (note)',
    limit_yn        CHAR(1) COMMENT '이용자 제한여부 (limitYn)',
    limit_detail    VARCHAR(100) COMMENT '이용제한 사유 (limitDetail)',
    del_yn          CHAR(1) COMMENT '삭제 여부 (delYn)',
    del_detail      VARCHAR(100) COMMENT '삭제 사유 (delDetail)',
    kind            VARCHAR(10) COMMENT '충전소 구분 코드 (kind)',
    kind_detail     VARCHAR(10) COMMENT '충전소 구분 상세코드 (kindDetail)',
    zcode           VARCHAR(5) COMMENT '지역코드 (zcode)',
    zscode          VARCHAR(10) COMMENT '지역상세코드 (zscode)',
    traffic_yn      CHAR(1) COMMENT '편의제공 여부 (trafficYn)',
    year            INT COMMENT '설치년도 (year)',
    floor_num       VARCHAR(10) COMMENT '층수 (floorNum)',
    floor_type      CHAR(1) COMMENT '지상/지하 구분 (floorType)',
    operator_id     VARCHAR(10) COMMENT '운영기관 ID',
    update_dt       DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '상태 갱신 시각'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_station_area ON charger_station(zcode, zscode);
CREATE INDEX idx_station_operator ON charger_station(operator_id);

-- ==========================================
-- 4. 충전기 상세 정보
-- ==========================================
CREATE TABLE charger_detail (
    charger_id      VARCHAR(20) PRIMARY KEY COMMENT '충전기 ID (chgerId)',
    station_id      VARCHAR(20) COMMENT '충전소 ID (statId)',
    charger_type    VARCHAR(10) COMMENT '충전기 타입 (chgerType)',
    output_kw       FLOAT COMMENT '충전용량 kW (output)',
    method          VARCHAR(10) COMMENT '충전방식 (method)',
    del_yn          CHAR(1) COMMENT '삭제여부 (delYn)',
    del_detail      VARCHAR(100) COMMENT '삭제 사유 (delDetail)',
    stat            INT COMMENT '충전기 상태 (stat)',
    stat_upd_dt     DATETIME COMMENT '상태갱신일시 (statUpdDt)',
    last_tsdt       DATETIME COMMENT '마지막 충전 시작일시 (lastTsdt)',
    last_tedt       DATETIME COMMENT '마지막 충전 종료일시 (lastTedt)',
    now_tsdt        DATETIME COMMENT '현재 충전중 시작일시 (nowTsdt)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_charger_station ON charger_detail(station_id);
CREATE INDEX idx_charger_status ON charger_detail(stat);

-- ==========================================
-- 5. 충전기 상태 이력
-- ==========================================
CREATE TABLE charger_status_log (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    charger_id    VARCHAR(20) COMMENT '충전기 ID',
    stat          INT COMMENT '충전 상태 (1~9)',
    stat_upd_dt   DATETIME COMMENT '상태 변경 시각'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_status_time ON charger_status_log(stat_upd_dt);
CREATE INDEX idx_status_charger ON charger_status_log(charger_id);

-- ==========================================
-- 6. 충전기 타입 코드 마스터
-- ==========================================
CREATE TABLE charger_meta (
    charger_type   VARCHAR(10) PRIMARY KEY COMMENT '충전기 타입 코드',
    description    VARCHAR(200) COMMENT '설명 (예: DC콤보, AC완속 등)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ==========================================
-- 7. 충전기 상태 정보 (charger_status)
-- ==========================================
CREATE TABLE charger_status (
    busi_id        VARCHAR(10) COMMENT '기관 아이디 (busiId)',
    station_id     VARCHAR(20) COMMENT '충전소ID (statId)',
    charger_id     VARCHAR(20) COMMENT '충전기ID (chgerId)',
    stat           INT COMMENT '충전기상태 (1:통신이상,2:대기,3:충전중,4:운영중지,5:점검중,9:미확인)',
    stat_upd_dt    DATETIME COMMENT '상태갱신일시 (statUpdDt)',
    last_tsdt      DATETIME COMMENT '마지막 충전 시작일시 (lastTsdt)',
    last_tedt      DATETIME COMMENT '마지막 충전 종료일시 (lastTedt)',
    now_tsdt       DATETIME COMMENT '현재 충전중 시작일시 (nowTsdt)',
    reg_dt         DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '등록일시',
    upd_dt         DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '갱신일시',
    PRIMARY KEY (station_id, charger_id, stat_upd_dt)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_status_station ON charger_status(station_id);
CREATE INDEX idx_status_charger ON charger_status(charger_id);
CREATE INDEX idx_status_state ON charger_status(stat);




INSERT INTO charger_meta VALUES
('01', 'DC차데모'),
('02', 'AC완속'),
('03', 'DC차데모+AC3상'),
('04', 'DC콤보'),
('05', 'DC차데모+DC콤보'),
('06', 'DC차데모+AC3상+DC콤보'),
('07', 'AC3상'),
('08', 'DC콤보(완속)'),
('09', 'NACS'),
('10', 'DC콤보+NACS');

