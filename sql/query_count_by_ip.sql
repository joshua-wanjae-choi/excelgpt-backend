-- IP 별 쿼리카운트
CREATE TABLE IF NOT EXISTS QUERY_COUNT_BY_IP (
    ID BIGINT NOT NULL AUTO_INCREMENT COMMENT '쿼리카운트_IP ID',
    IP VARCHAR(20) NOT NULL COMMENT 'IP',
    QUERY_COUNT BIGINT NOT NULL COMMENT '날짜 별 쿼리 수',
    CREATE_DATETIME DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성시각',
    UPDATE_DATETIME DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '갱신시각',
    PRIMARY KEY (ID),
    UNIQUE (IP, CREATE_DATETIME)
) COMMENT = "IP 별 쿼리카운트"
;