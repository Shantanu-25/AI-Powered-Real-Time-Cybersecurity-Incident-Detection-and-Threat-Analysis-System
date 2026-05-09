import threading
import time
import asyncio
from scapy.all import sniff, IP, TCP, UDP
import logging
from ml.model import ml_engine
from database.mongodb import get_db
from schemas.cyber_schema import ThreatCreate
from datetime import datetime

logger = logging.getLogger(__name__)

class PacketCaptureService:
    def __init__(self):
        self.is_capturing = False
        self.capture_thread = None
        self.packet_count = 0
        
        # Simple feature tracking window
        self.recent_packets = []
        self.window_size = 5 # seconds

    def process_packet(self, packet):
        self.packet_count += 1
        
        # In a real scenario, this would extract complex features over a time window
        # For MVP, we extract basic info and simulate some features
        
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            proto = packet[IP].proto
            length = len(packet)
            
            # Simulate features for ML prediction
            features = [
                1.5, # packet_rate (simulated)
                proto, # protocol_type
                10, # connection_count
                length, # packet_size
                1 if TCP in packet and packet[TCP].flags == 'S' else 0, # syn_count
                0, # failed_login_count
                0.1 # session_duration
            ]
            
            import numpy as np
            prediction = ml_engine.predict(np.array([features]))
            
            if prediction["attack_type"] != "Normal" and prediction["risk_score"] > 0.6:
                logger.warning(f"Threat Detected: {prediction['attack_type']} from {src_ip}")
                
                # Asynchronously save to DB
                # Note: creating a new event loop in a thread can be tricky, 
                # so we might use a queue to send to main async loop in a full prod app.
                # For MVP, we'll log it.
                
                # Async execution helper
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                loop.run_until_complete(self.save_threat(
                    ThreatCreate(
                        source_ip=src_ip,
                        destination_ip=dst_ip,
                        attack_type=prediction["attack_type"],
                        severity="High" if prediction["risk_score"] > 0.8 else "Medium",
                        risk_score=prediction["risk_score"],
                        protocol=str(proto),
                        details=f"Detected anomaly in packet from {src_ip} to {dst_ip}"
                    )
                ))

    async def save_threat(self, threat: ThreatCreate):
        db = get_db()
        await db.threats.insert_one(threat.dict())

    def start_capture(self, interface=None):
        if self.is_capturing:
            return False
            
        self.is_capturing = True
        logger.info("Starting packet capture...")
        
        def capture_loop():
            # sniff runs until stop_filter returns True
            sniff(prn=self.process_packet, store=0, stop_filter=lambda x: not self.is_capturing, iface=interface)
            
        self.capture_thread = threading.Thread(target=capture_loop)
        self.capture_thread.start()
        return True

    def stop_capture(self):
        if not self.is_capturing:
            return False
            
        logger.info("Stopping packet capture...")
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        return True

capture_service = PacketCaptureService()
