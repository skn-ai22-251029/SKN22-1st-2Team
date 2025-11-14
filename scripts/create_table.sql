-- Active: 1762504481605@@127.0.0.1@3306@grilled_kim
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
    zcode       VARCHAR(2)   NOT NULL COMMENT '시도 코드',
    zscode      VARCHAR(5)   NOT NULL COMMENT '시군구 코드 (행정구역코드 앞 2자리 + 법정동코드 3자리)',
    region      VARCHAR(50)  NOT NULL COMMENT '시도명',
    sub_region  VARCHAR(50)  NOT NULL COMMENT '시군구명',
    reg_dt      DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '등록일자',
    upd_dt      DATETIME     ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일자',
    PRIMARY KEY (zcode, zscode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='전국 지역 코드 마스터';


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

-- ==========================================
-- 8. 요금 정보 테이블
-- ==========================================
CREATE TABLE charge_price (
    operator_name VARCHAR(100) NOT NULL,
    rnum DECIMAL(10,2),
    price_type_name VARCHAR(20)  ,
    update_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    price_type_code VARCHAR(10) NOT NULL,
    member_price VARCHAR(20)  ,
    operator_code VARCHAR(20) NOT NULL,
    guest_price VARCHAR(20) NOT NULL,

    PRIMARY KEY (operator_code, price_type_code)
);
# 충전 단자 코드
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

insert into charger_meta values
('11', 'DC콤보2(버스전용)');


# 지역코드
INSERT INTO area_code_master (zcode, zscode, region, sub_region) VALUES
-- 서울특별시 (11)
('11', '11110', '서울특별시', '종로구'),
('11', '11140', '서울특별시', '중구'),
('11', '11170', '서울특별시', '용산구'),
('11', '11200', '서울특별시', '성동구'),
('11', '11215', '서울특별시', '광진구'),
('11', '11230', '서울특별시', '동대문구'),
('11', '11260', '서울특별시', '중랑구'),
('11', '11290', '서울특별시', '성북구'),
('11', '11305', '서울특별시', '강북구'),
('11', '11320', '서울특별시', '도봉구'),
('11', '11350', '서울특별시', '노원구'),
('11', '11380', '서울특별시', '은평구'),
('11', '11410', '서울특별시', '서대문구'),
('11', '11440', '서울특별시', '마포구'),
('11', '11470', '서울특별시', '양천구'),
('11', '11500', '서울특별시', '강서구'),
('11', '11530', '서울특별시', '구로구'),
('11', '11545', '서울특별시', '금천구'),
('11', '11560', '서울특별시', '영등포구'),
('11', '11590', '서울특별시', '동작구'),
('11', '11620', '서울특별시', '관악구'),
('11', '11650', '서울특별시', '서초구'),
('11', '11680', '서울특별시', '강남구'),
('11', '11710', '서울특별시', '송파구'),
('11', '11740', '서울특별시', '강동구'),
-- 부산광역시 (26)
('26', '26110', '부산광역시', '중구'),
('26', '26140', '부산광역시', '서구'),
('26', '26170', '부산광역시', '동구'),
('26', '26200', '부산광역시', '영도구'),
('26', '26230', '부산광역시', '부산진구'),
('26', '26260', '부산광역시', '동래구'),
('26', '26290', '부산광역시', '남구'),
('26', '26320', '부산광역시', '북구'),
('26', '26350', '부산광역시', '해운대구'),
('26', '26380', '부산광역시', '사하구'),
('26', '26410', '부산광역시', '금정구'),
('26', '26440', '부산광역시', '강서구'),
('26', '26470', '부산광역시', '연제구'),
('26', '26500', '부산광역시', '수영구'),
('26', '26530', '부산광역시', '사상구'),
('26', '26710', '부산광역시', '기장군'),
-- 대구광역시 (27)
('27', '27110', '대구광역시', '중구'),
('27', '27140', '대구광역시', '동구'),
('27', '27170', '대구광역시', '서구'),
('27', '27200', '대구광역시', '남구'),
('27', '27230', '대구광역시', '북구'),
('27', '27260', '대구광역시', '수성구'),
('27', '27290', '대구광역시', '달서구'),
('27', '27710', '대구광역시', '달성군'),
-- 인천광역시 (28)
('28', '28110', '인천광역시', '중구'),
('28', '28140', '인천광역시', '동구'),
('28', '28177', '인천광역시', '미추홀구'),
('28', '28185', '인천광역시', '연수구'),
('28', '28200', '인천광역시', '남동구'),
('28', '28237', '인천광역시', '부평구'),
('28', '28245', '인천광역시', '계양구'),
('28', '28260', '인천광역시', '서구'),
('28', '28710', '인천광역시', '강화군'),
('28', '28720', '인천광역시', '옹진군'),
-- 광주광역시 (29)
('29', '29110', '광주광역시', '동구'),
('29', '29140', '광주광역시', '서구'),
('29', '29155', '광주광역시', '남구'),
('29', '29170', '광주광역시', '북구'),
('29', '29200', '광주광역시', '광산구'),
-- 대전광역시 (30)
('30', '30110', '대전광역시', '동구'),
('30', '30140', '대전광역시', '중구'),
('30', '30170', '대전광역시', '서구'),
('30', '30200', '대전광역시', '유성구'),
('30', '30230', '대전광역시', '대덕구'),
-- 울산광역시 (31)
('31', '31110', '울산광역시', '중구'),
('31', '31140', '울산광역시', '남구'),
('31', '31170', '울산광역시', '동구'),
('31', '31200', '울산광역시', '북구'),
('31', '31710', '울산광역시', '울주군'),
-- 세종특별자치시 (36)
('36', '36110', '세종특별자치시', '세종시'),
-- 경기도 (41)
('41', '41110', '경기도', '수원시'),
('41', '41113', '경기도', '수원시 장안구'),
('41', '41115', '경기도', '수원시 권선구'),
('41', '41117', '경기도', '수원시 팔달구'),
('41', '41119', '경기도', '수원시 영통구'),
('41', '41130', '경기도', '성남시'),
('41', '41131', '경기도', '성남시 수정구'),
('41', '41133', '경기도', '성남시 중원구'),
('41', '41135', '경기도', '성남시 분당구'),
('41', '41150', '경기도', '의정부시'),
('41', '41170', '경기도', '안양시'),
('41', '41171', '경기도', '안양시 만안구'),
('41', '41173', '경기도', '안양시 동안구'),
('41', '41190', '경기도', '부천시'),
('41', '41210', '경기도', '광명시'),
('41', '41220', '경기도', '평택시'),
('41', '41250', '경기도', '동두천시'),
('41', '41270', '경기도', '안산시'),
('41', '41271', '경기도', '안산시 상록구'),
('41', '41273', '경기도', '안산시 단원구'),
('41', '41280', '경기도', '고양시'),
('41', '41281', '경기도', '고양시 덕양구'),
('41', '41285', '경기도', '고양시 일산동구'),
('41', '41287', '경기도', '고양시 일산서구'),
('41', '41290', '경기도', '과천시'),
('41', '41310', '경기도', '구리시'),
('41', '41360', '경기도', '남양주시'),
('41', '41370', '경기도', '오산시'),
('41', '41390', '경기도', '시흥시'),
('41', '41410', '경기도', '군포시'),
('41', '41430', '경기도', '의왕시'),
('41', '41450', '경기도', '하남시'),
('41', '41460', '경기도', '용인시'),
('41', '41461', '경기도', '용인시 처인구'),
('41', '41463', '경기도', '용인시 기흥구'),
('41', '41465', '경기도', '용인시 수지구'),
('41', '41480', '경기도', '파주시'),
('41', '41500', '경기도', '이천시'),
('41', '41550', '경기도', '안성시'),
('41', '41570', '경기도', '김포시'),
('41', '41590', '경기도', '화성시'),
('41', '41610', '경기도', '광주시'),
('41', '41630', '경기도', '양주시'),
('41', '41650', '경기도', '포천시'),
('41', '41670', '경기도', '여주시'),
('41', '41800', '경기도', '연천군'),
('41', '41820', '경기도', '가평군'),
('41', '41830', '경기도', '양평군');
