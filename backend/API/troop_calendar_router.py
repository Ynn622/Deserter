from fastapi import APIRouter, HTTPException, Query

from services.troop_calendar import get_troop_calendar


router = APIRouter(prefix="/troop-calendar", tags=["入伍行事曆"])


@router.get("")
def get_calendar(
    branch: str | None = Query(default=None, description="軍種"),
    schedule_id: str | None = Query(default=None, description="梯次資料 ID"),
):
    try:
        payload = get_troop_calendar()
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"入伍行事曆暫時無法更新：{error}",
        ) from error

    schedules = payload["schedules"]
    if branch:
        schedules = [item for item in schedules if item["branch"] == branch]
    if schedule_id:
        schedules = [item for item in schedules if item["id"] == schedule_id]
        if not schedules:
            raise HTTPException(status_code=404, detail="找不到指定梯次")

    return {
        **payload,
        "branches": ["陸軍", "海軍艦艇兵", "海軍陸戰隊", "空軍"],
        "count": len(schedules),
        "schedules": schedules,
    }
