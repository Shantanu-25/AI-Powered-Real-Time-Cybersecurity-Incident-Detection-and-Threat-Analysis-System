from fastapi import APIRouter, Query
from typing import List, Optional
from database.mongodb import get_db
from schemas.cyber_schema import ThreatResponse

router = APIRouter()

@router.get("/live", response_model=List[ThreatResponse])
async def get_live_threats(limit: int = Query(10, le=100)):
    """Get the most recent threats"""
    db = get_db()
    cursor = db.threats.find().sort("timestamp", -1).limit(limit)
    threats = await cursor.to_list(length=limit)
    
    # Map _id to id
    for t in threats:
        t["id"] = str(t.pop("_id"))
    return threats

@router.get("/history", response_model=List[ThreatResponse])
async def get_threat_history(
    skip: int = 0, 
    limit: int = 100,
    min_severity: Optional[str] = None
):
    """Get historical threats with optional filtering"""
    db = get_db()
    query = {}
    if min_severity:
        query["severity"] = min_severity
        
    cursor = db.threats.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    threats = await cursor.to_list(length=limit)
    
    for t in threats:
        t["id"] = str(t.pop("_id"))
    return threats
