-- 공용코드
CREATE TABLE IF NOT EXISTS `COMMON_CODE` (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '공용코드 ID',
    code VARCHAR(150) COMMENT '공용코드',
    description VARCHAR(255) COMMENT '공용코드 설명',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성시각',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '갱신시각',
    PRIMARY KEY (id),
    UNIQUE (code)
) COMMENT = "공용코드"
;


-- IP 별 쿼리카운트
CREATE TABLE IF NOT EXISTS QUERY_COUNT_BY_IP (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '쿼리카운트_IP ID',
    ip VARCHAR(20) NOT NULL COMMENT 'IP',
    query_count BIGINT NOT NULL COMMENT '날짜 별 쿼리 수',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성시각',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '갱신시각',
    PRIMARY KEY (id),
    UNIQUE (ip, created_at)
) COMMENT = "IP 별 쿼리카운트"
;

-- 쿼리 스니펫
CREATE TABLE IF NOT EXISTS QUERY_SNIPPET (
    id BIGINT NOT NULL AUTO_INCREMENT COMMENT '쿼리 스니펫 ID',
    common_code VARCHAR(150) NOT NULL COMMENT '쿼리 스니펫 코드',
    snippet text NOT NULL COMMENT '쿼리 스니펫',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성시각',
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '갱신시각',
    PRIMARY KEY (id),
    UNIQUE (common_code),
    FOREIGN KEY (common_code) REFERENCES `COMMON_CODE` (code)
) COMMENT = "쿼리 스니펫"
;

INSERT INTO COMMON_CODE (code, description)
VALUES
('table-query-snippet', '테이블 쿼리 스니펫'),
('constraint-query-snippet', '제약조건 쿼리 스니펫');

INSERT INTO QUERY_SNIPPET (COMMON_CODE, SNIPPET) 
VALUES
('table-query-snippet', '
Dataframe name is %file_name%.
File path is "%path%".
Data of %file_name% = `
%lines%
`.
First line of %file_name% is header. 
Delimiter of %file_name% is "|". 
Extension of %file_name% not exists. 
Index_col of %file_name% is False. 
Replace NaN fields with empty strings.
        
');

INSERT INTO QUERY_SNIPPET (COMMON_CODE, SNIPPET) 
VALUES
('constraint-query-snippet', '
Result dataframe is named %result_file_name%. 
Result file path is %result_path%. 
Delimiter of %result_file_name% is "|". 
Result file of extension not exists. 

Request below. 
%query% 
Extract only existing columns of %base_sheet_name%. 

Constraints below. 
Using python, pandas and do not print results. 

');