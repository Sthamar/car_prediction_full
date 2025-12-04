import pandas as pd
import numpy as np
import random

np.random.seed(42)

makes_models = {
    "Suzuki": ["Alto", "Wagon R", "Baleno", "Swift"],
    "Hyundai": ["i10", "i20", "Creta", "Venue"],
    "Kia": ["Sportage", "Seltos", "Sonet"],
    "Tata": ["Tiago", "Nexon", "Altroz"],
    "Mahindra": ["Scorpio", "Bolero", "XUV300"],
    "Toyota": ["Yaris", "Corolla", "Hilux"]
}

terrain_options = ["Urban", "Highway", "Hills"]
driving_styles = ["rough", "normal", "smooth"]
fuel_types = ["Petrol", "Diesel"]
transmissions = ["Manual", "Automatic"]

def generate_row():
    make = random.choice(list(makes_models.keys()))
    model = random.choice(makes_models[make])

    year = np.random.randint(1998, 2024)
    mileage = np.random.randint(3000, 200000)
    engine_size = round(np.random.uniform(0.8, 2.4), 1)
    transmission = random.choice(transmissions)
    fuel_type = random.choice(fuel_types)
    terrain = random.choice(terrain_options)
    road_quality = np.random.randint(1, 6)  # 1–5
    days_since_service = np.random.randint(0, 600)
    driving_style = random.choice(driving_styles)

    # Nepal-based service need probability
    risk = 0

    # 🔥 Mileage based rule
    if mileage % 10000 < 1500:
        risk += 0.25

    # 🔥 Service overdue
    if days_since_service > 180:
        risk += 0.35

    # 🔥 Terrain effect
    if terrain == "Hills":
        risk += 0.2

    # 🔥 Road quality effect
    if road_quality <= 2:
        risk += 0.15

    # 🔥 Driving style
    if driving_style == "rough":
        risk += 0.2

    # 🔥 Diesel cars older than 10 years
    if fuel_type == "Diesel" and (2024 - year) > 10:
        risk += 0.25

    service_needed = 1 if risk > 0.45 else 0

    return [
        make, model, year, mileage, engine_size, transmission, fuel_type,
        terrain, road_quality, days_since_service, driving_style, service_needed
    ]

rows = [generate_row() for _ in range(10000)]

df = pd.DataFrame(rows, columns=[
    "make", "model", "year", "mileage", "engine_size", "transmission", "fuel_type",
    "terrain_type", "avg_road_quality", "days_since_service", "driving_style", "service_needed"
])

df.to_csv("ml/dataset_nepal.csv", index=False)

print("Generated dataset_nepal.csv")
