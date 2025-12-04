from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app import models, database
from app.schemas import CarData, PredictionResponse
from app.predictor import ServicePredictor
from app.routers import auth, users, vehicles, predictions, services, catalog

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Car Service Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(vehicles.router)
app.include_router(predictions.router)
app.include_router(services.router)
app.include_router(catalog.router)

predictor = ServicePredictor()


@app.get("/")
def root():
    return {"message": "Car Service Prediction API", "version": "2.0"}


@app.post("/predict", response_model=PredictionResponse)
def predict_service(car: CarData):
    try:
        return predictor.predict(car)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "healthy"}
