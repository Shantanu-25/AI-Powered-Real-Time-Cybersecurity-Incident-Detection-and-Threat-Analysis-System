from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from ml.model import ml_engine
from core.config import settings

router = APIRouter()

class FeatureInput(BaseModel):
    packet_rate: float
    protocol_type: int
    connection_count: int
    packet_size: int
    syn_count: int
    failed_login_count: int
    session_duration: float

@router.post("/predict")
async def predict_threat(features: FeatureInput):
    """Predict if the given network features constitute a threat"""
    try:
        # Convert to numpy array for prediction
        feature_array = np.array([[
            features.packet_rate,
            features.protocol_type,
            features.connection_count,
            features.packet_size,
            features.syn_count,
            features.failed_login_count,
            features.session_duration
        ]])
        
        prediction = ml_engine.predict(feature_array)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train")
async def train_model(background_tasks: BackgroundTasks):
    """Trigger model retraining with synthetic or available dataset"""
    
    # In a real scenario, you'd load from DB or a CSV
    # Here we generate synthetic data for the MVP to run out-of-the-box
    def train_synthetic():
        # Generate some synthetic data representing the 6 classes (Normal + 5 attacks)
        # Features: packet_rate, protocol_type, connection_count, packet_size, syn_count, failed_login_count, session_duration
        np.random.seed(42)
        n_samples = 1000
        
        X = np.random.rand(n_samples, 7)
        # Add some patterns
        # 1: Port Scan (high connection count, low packet size, high syn count)
        X[100:200, 2] += 2.0
        X[100:200, 3] *= 0.1
        X[100:200, 4] += 1.5
        
        # 2: Brute Force (high failed login)
        X[200:300, 5] += 3.0
        
        # 3: DDoS (extreme packet rate, connection count)
        X[300:400, 0] += 4.0
        X[300:400, 2] += 3.0
        
        # Labels
        y = np.zeros(n_samples)
        y[100:200] = 1 # Port Scan
        y[200:300] = 2 # Brute Force
        y[300:400] = 3 # DDoS
        y[400:500] = 4 # Packet Flood
        y[500:600] = 5 # Anomalous
        
        df_X = pd.DataFrame(X)
        series_y = pd.Series(y)
        
        ml_engine.train(df_X, series_y)
        print("Model training completed on synthetic data")

    background_tasks.add_task(train_synthetic)
    return {"message": "Model training started in background"}
