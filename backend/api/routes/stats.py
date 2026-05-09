from fastapi import APIRouter
from database.mongodb import get_db

router = APIRouter()

@router.get("/")
async def get_system_stats():
    """Get overall system statistics for the dashboard"""
    db = get_db()
    
    total_threats = await db.threats.count_documents({})
    high_severity = await db.threats.count_documents({"severity": "High"})
    
    # Get threat type distribution
    pipeline = [
        {"$group": {"_id": "$attack_type", "count": {"$sum": 1}}}
    ]
    distribution_cursor = db.threats.aggregate(pipeline)
    distribution = await distribution_cursor.to_list(length=None)
    
    # Format distribution for frontend
    dist_dict = {item["_id"]: item["count"] for item in distribution}
    
    return {
        "total_threats_detected": total_threats,
        "high_severity_threats": high_severity,
        "threat_distribution": dist_dict,
        "system_status": "Healthy",
        "capture_active": True # In reality, query the capture service
    }
