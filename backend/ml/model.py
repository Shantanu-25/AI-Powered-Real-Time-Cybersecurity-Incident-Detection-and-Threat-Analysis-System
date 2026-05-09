import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatDetectionModel:
    def __init__(self, model_path: str = "random_forest_model.joblib"):
        self.model_path = model_path
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.is_trained = True
                logger.info(f"Loaded existing model from {self.model_path}")
            except Exception as e:
                logger.error(f"Error loading model: {e}")

    def train(self, X: pd.DataFrame, y: pd.Series):
        """Train the model with new data"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logger.info("Training Random Forest Classifier...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        predictions = self.model.predict(X_test)
        
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average='weighted', zero_division=0),
            "recall": recall_score(y_test, predictions, average='weighted', zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, predictions).tolist()
        }
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path) if os.path.dirname(self.model_path) else '.', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
        
        return metrics

    def predict(self, features: np.ndarray) -> dict:
        """Predict threat and risk score based on features"""
        if not self.is_trained:
            logger.warning("Model is not trained. Returning dummy prediction.")
            return {"attack_type": "Normal", "risk_score": 0.0}

        # Predict class
        prediction = self.model.predict(features)[0]
        
        # Predict probability
        probabilities = self.model.predict_proba(features)[0]
        max_prob = float(max(probabilities))
        
        # Map output to threat types (Example mapping)
        class_mapping = {
            0: "Normal",
            1: "Port Scanning",
            2: "Brute Force",
            3: "DDoS",
            4: "Packet Flooding",
            5: "Anomalous Traffic"
        }
        
        attack_type = class_mapping.get(prediction, "Unknown")
        
        return {
            "attack_type": attack_type,
            "risk_score": max_prob if attack_type != "Normal" else 0.0
        }

# Singleton instance
ml_engine = ThreatDetectionModel()
