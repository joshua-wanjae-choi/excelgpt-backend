from dto.response_dto import ResponseDto
import dataclasses

class Response:
    _resonse_map = {
        "0000": {
            "kr": "성공",
        },
        "3000": {
            "kr": "허루 허용 요청 수 초과"
        },
        "7000": {
            "kr": "파일 동기화 실패"
        }, 
        "7100": {
            "kr": "쿼리 요청 실패"
        }, 
        "7101": {
            "kr": "쿼리 실행 실패"
        }, 
        "9999": {
            "kr": "알 수 없는 에러 발생"
        }, 
    }
    
    @staticmethod
    def get_response(code: str, lang: str = None):
        default_lang = "kr"
        row = Response._resonse_map["9999"]
        if code in Response._resonse_map:
            row = Response._resonse_map[code]
            
        result = ResponseDto(code=code, lang=default_lang, message=row[default_lang])
        if lang is not None:
            result = ResponseDto(code=code, lang=lang, message=row[lang])

        return dataclasses.asdict(result)
