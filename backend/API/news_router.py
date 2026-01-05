from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from util.logger import log_print
from util.nowtime import TaiwanTime

from services.news_data import news_summary

router = APIRouter(prefix="/news", tags=["新聞資料 News"])

@router.get("/summary")
@log_print
def get_all_news_summary(keyword: str, page: int = 1):
    """
    取得指定股票「新聞」資料的摘要。
    """
    news_summary_df = news_summary(keyword, page=page)
    result = news_summary_df.to_dict(orient='records')
    return JSONResponse(content={'news': result, 'updateTime': TaiwanTime.string()})

