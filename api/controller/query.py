from fastapi import APIRouter
from pydantic import BaseModel
from service.answer import get_answer


router = APIRouter(prefix="/query")


class RequestQueryBody(BaseModel):
    query: str


@router.post("")
def request_query(request_query_body: RequestQueryBody):
    return get_answer(request_query_body.query)
