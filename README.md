# AI-Powered Real-Time Cybersecurity Incident Detection and Threat Analysis System

## Overview
This is a comprehensive MVP for a real-time cybersecurity monitoring platform. It captures network traffic, uses Machine Learning (Random Forest) to detect threats in real-time, and visualizes incidents on a modern Security Operations Center (SOC) dashboard.

## System Architecture

Live Network Traffic -> Packet Capture Engine (Scapy) -> Feature Extraction -> ML Threat Detection Engine (Random Forest) -> Threat Classification & Risk Scoring -> Alert Automation (Email/Telegram) -> Dashboard Visualization (Streamlit) -> MongoDB Logging

## Features
- **Real-time Packet Capture**: Analyzes incoming/outgoing packets.
- **Machine Learning Detection**: Identifies Port Scanning, Brute Force, DDoS, and Anomalous Traffic.
- **Automated Alerts**: Triggers notifications for high-risk threats.
- **SOC Dashboard**: Modern, dark-themed UI with real-time metrics and charts.
- **REST API**: Built with FastAPI for high performance.
- **Dockerized Environment**: Ready for production deployment.

## Project Structure
```
project/
│
├── backend/                  # FastAPI Application
│   ├── api/routes/           # API Endpoints
│   ├── core/                 # Configuration
│   ├── database/             # MongoDB Connection
│   ├── ml/                   # Machine Learning Model
│   ├── schemas/              # Pydantic Models
│   ├── services/             # Capture & Alert Logic
│   └── main.py               # Entry Point
│
├── frontend/                 # Streamlit Dashboard
│   ├── app.py
│   └── Dockerfile
│
├── .env.example              # Environment variables template
├── docker-compose.yml        # Docker composition
└── README.md
```

## Prerequisites
- Docker and Docker Compose
- Python 3.11 (if running locally without Docker)

## Setup and Installation

### Method 1: Using Docker (Recommended)

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in the required variables (especially for alerts).
   ```bash
   cp .env.example .env
   ```
3. Build and run the containers:
   ```bash
   docker-compose up --build -d
   ```
4. Access the applications:
   - Dashboard: http://localhost:8501
   - API Docs: http://localhost:8000/docs

### Method 2: Running Locally (Development)

1. **Start MongoDB**: Ensure you have a local MongoDB instance running on port 27017.
2. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
3. **Frontend Setup**:
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Testing & Usage

### Phase 1: Dashboard & ML Training Initialization
1. Open the **Dashboard**: [http://localhost:8501](http://localhost:8501).
2. Look at the left sidebar. Under **"ML Model"**, click **"🔄 Retrain Model"**. 
   *(This tells the backend to generate a synthetic dataset of regular traffic and 5 types of attacks, and trains the Random Forest model on the spot).*
3. Wait for the toast notification saying "Model retraining initiated".

### Phase 2: Starting the Packet Capture
1. In the sidebar, under **"Capture Engine"**, click **"▶ Start"**.
2. The "Capture Engine" metric card on the dashboard should now say **"Active"**.
   *(The system is now actively listening to network packets).*

### Phase 3: Triggering a Threat Detection
Because Docker creates an isolated virtual network, running a real attack (like a port scan) from your Windows machine won't easily reach the Docker container's internal network sniffer without advanced bridging. However, we can test the **AI Engine** directly by simulating malicious packet features!

1. Open the **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
2. Scroll down to the green **`POST /api/v1/model/predict`** box and click on it.
3. Click **"Try it out"** (top right corner of the box).
4. In the Request body, paste this JSON to simulate a **DDoS Attack** (High packet rate & high connection count):
   ```json
   {
     "packet_rate": 5.5,
     "protocol_type": 6,
     "connection_count": 100,
     "packet_size": 40,
     "syn_count": 50,
     "failed_login_count": 0,
     "session_duration": 0.5
   }
   ```
5. Click **Execute**. 
6. Look at the Response body below. You should see the AI accurately detecting the `"attack_type"` as "DDoS" and assigning a high `"risk_score"`.

### Phase 4: Seeing it Live
1. Go back to your Streamlit Dashboard: [http://localhost:8501](http://localhost:8501)
2. Click the **"🔄 Refresh Data"** button at the very bottom.
3. You will now see:
   - Your "Total Threats" and "High Severity" numbers increased.
   - The Threat Distribution Pie Chart updated.
   - The Risk Score Gauge updated.
   - The threat appearing in the **🔴 Live Threat Feed** table!

## API Documentation
- `POST /api/v1/capture/start`: Start packet capture.
- `POST /api/v1/capture/stop`: Stop packet capture.
- `GET /api/v1/threats/live`: Get recent threats.
- `GET /api/v1/stats`: Get dashboard statistics.
- `POST /api/v1/model/predict`: Predict threat from features.
- `POST /api/v1/model/train`: Retrain the ML model.

## Future Scope
- Integration with Suricata or Zeek for advanced packet analysis.
- Implementing an auto-firewall blocking mechanism.
- Advanced AI models (e.g., LSTMs for time-series anomaly detection).
- User authentication and Role-Based Access Control (RBAC).
