import joblib
import numpy as np
import pandas as pd
from datetime import datetime

class ServicePredictor:
    def __init__(self):
        self.model = joblib.load("ml/model.pkl")
        self.scaler = joblib.load("ml/scaler.pkl")

    def preprocess(self, data):
        df = pd.DataFrame([{
            "year": data.year,
            "mileage": data.mileage,
            "engine_size": data.engine_size,
            "days_since_service": (datetime.now() - datetime.strptime(data.last_service_date, "%Y-%m-%d")).days
        }])

        # Scale numerical features
        scaled = self.scaler.transform(df)
        return scaled

    def predict(self, data):
        X = self.preprocess(data)
        prob = self.model.predict_proba(X)[0][1]  # probability service needed
        service_needed = prob > 0.55

        # Recommendation logic
        recommended = []
        days_since = (datetime.now() - datetime.strptime(data.last_service_date, "%Y-%m-%d")).days

        if data.mileage % 10000 < 1500:
            recommended.append("Oil Change")

        if days_since > 180:
            recommended.append("Routine Inspection")

        if data.mileage > 120000:
            recommended.append("Transmission Check")

        if not recommended:
            recommended.append("No immediate service required")

        # Risk level
        risk_level = "High" if prob > 0.75 else "Medium" if prob > 0.50 else "Low"

        estimated_days =  max(0, int(200 - days_since))

        return {
            "service_needed": service_needed,
            "confidence": round(float(prob), 2),
            "estimated_days_until_service": estimated_days,
            "recommended_services": recommended,
            "risk_level": risk_level
        }
