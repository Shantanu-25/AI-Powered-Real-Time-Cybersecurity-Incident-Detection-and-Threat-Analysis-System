from fastapi import APIRouter
from database.mongodb import get_db

router = APIRouter()

@router.get("/")
async def get_alerts(limit: int = 50):
    """Get recent alerts"""
    db = get_db()
    cursor = db.alerts.find().sort("timestamp", -1).limit(limit)
    alerts = await cursor.to_list(length=limit)
    
    for a in alerts:
        a["id"] = str(a.pop("_id"))
    return alerts
