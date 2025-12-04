from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app import auth, models, schemas

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/save", response_model=schemas.PredictionHistoryResponse)
def save_prediction(
    prediction: schemas.PredictionHistoryCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    db_prediction = models.PredictionHistory(
        **prediction.dict(),
        user_id=current_user.id
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

@router.get("/history", response_model=List[schemas.PredictionHistoryResponse])
def get_prediction_history(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: int = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    query = db.query(models.PredictionHistory).filter(
        models.PredictionHistory.user_id == current_user.id
    )
    
    if vehicle_id:
        query = query.filter(models.PredictionHistory.vehicle_id == vehicle_id)
    
    predictions = query.order_by(
        models.PredictionHistory.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return predictions

@router.get("/stats", response_model=schemas.UserStatistics)
def get_user_statistics(
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    # Total predictions
    total_predictions = db.query(func.count(models.PredictionHistory.id)).filter(
        models.PredictionHistory.user_id == current_user.id
    ).scalar()
    
    # Total vehicles
    total_vehicles = db.query(func.count(models.Vehicle.id)).filter(
        models.Vehicle.user_id == current_user.id
    ).scalar()
    
    # Total services
    total_services = db.query(func.count(models.ServiceRecord.id)).filter(
        models.ServiceRecord.user_id == current_user.id
    ).scalar()
    
    # Predictions this month
    current_month = datetime.now().month
    current_year = datetime.now().year
    predictions_this_month = db.query(func.count(models.PredictionHistory.id)).filter(
        models.PredictionHistory.user_id == current_user.id,
        extract('month', models.PredictionHistory.created_at) == current_month,
        extract('year', models.PredictionHistory.created_at) == current_year
    ).scalar()
    
    # Upcoming services (predictions with service needed in next 30 days)
    upcoming_services = db.query(func.count(models.PredictionHistory.id)).filter(
        models.PredictionHistory.user_id == current_user.id,
        models.PredictionHistory.service_needed == True,
        models.PredictionHistory.estimated_days_until_service <= 30,
        models.PredictionHistory.estimated_days_until_service >= 0
    ).scalar()
    
    return schemas.UserStatistics(
        total_predictions=total_predictions or 0,
        total_vehicles=total_vehicles or 0,
        total_services=total_services or 0,
        predictions_this_month=predictions_this_month or 0,
        upcoming_services=upcoming_services or 0
    )

@router.get("/{prediction_id}", response_model=schemas.PredictionHistoryResponse)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    prediction = db.query(models.PredictionHistory).filter(
        models.PredictionHistory.id == prediction_id,
        models.PredictionHistory.user_id == current_user.id
    ).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
