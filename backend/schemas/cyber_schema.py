from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ThreatCreate(BaseModel):
    source_ip: str
    destination_ip: str
    attack_type: str
    severity: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    risk_score: float
    protocol: str
    details: Optional[str] = None

class ThreatResponse(ThreatCreate):
    id: str

class PacketFeature(BaseModel):
    packet_rate: float
    protocol_type: int
    connection_count: int
    packet_size: int
    syn_count: int
    failed_login_count: int
    session_duration: float

class AlertCreate(BaseModel):
    threat_id: Optional[str] = None
    message: str
    level: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
