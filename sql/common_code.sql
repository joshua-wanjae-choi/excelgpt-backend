-- 공용코드
CREATE TABLE IF NOT EXISTS `COMMON_CODE` (
    ID BIGINT NOT NULL AUTO_INCREMENT COMMENT '공용코드 ID',
    CODE VARCHAR(150) COMMENT '공용코드',
    DESCRIPTION VARCHAR(255) COMMENT '공용코드 설명',
    CREATE_DATETIME DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성시각',
    UPDATE_DATETIME DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '갱신시각',
    PRIMARY KEY (ID),
    UNIQUE (CODE)
) COMMENT = "공용코드"
;