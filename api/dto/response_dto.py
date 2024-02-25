from dataclasses import dataclass

@dataclass
class ResponseDto:
    code: str
    lang: str
    message: str
