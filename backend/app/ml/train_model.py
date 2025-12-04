import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build path to dataset
dataset_path = os.path.join(BASE_DIR, "dataset_nepal.csv")
df = pd.read_csv(dataset_path)

# Select features and label
X = df[["year", "mileage", "engine_size", "days_since_service"]]
y = df["service_needed"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_scaled, y)

# Save model and scaler in the same folder as the script
joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(scaler, os.path.join(BASE_DIR, "scaler.pkl"))

print("Training completed. model.pkl and scaler.pkl saved in", BASE_DIR)
