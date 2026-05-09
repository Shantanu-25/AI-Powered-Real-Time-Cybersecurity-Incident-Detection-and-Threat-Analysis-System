from fastapi import APIRouter, HTTPException
from services.capture_service import capture_service

router = APIRouter()

@router.post("/start")
async def start_capture():
    """Start real-time packet capture"""
    success = capture_service.start_capture()
    if not success:
        return {"status": "info", "message": "Capture is already running"}
    return {"status": "success", "message": "Packet capture started"}

@router.post("/stop")
async def stop_capture():
    """Stop real-time packet capture"""
    success = capture_service.stop_capture()
    if not success:
        return {"status": "info", "message": "Capture is not running"}
    return {"status": "success", "message": "Packet capture stopped"}

@router.get("/status")
async def capture_status():
    """Get capture engine status"""
    return {
        "is_capturing": capture_service.is_capturing,
        "packets_processed": capture_service.packet_count
    }
