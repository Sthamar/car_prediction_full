from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import auth, models, schemas

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=schemas.ServiceRecordResponse)
def create_service_record(
    service: schemas.ServiceRecordCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    db_service = models.ServiceRecord(
        **service.dict(),
        user_id=current_user.id
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/", response_model=List[schemas.ServiceRecordResponse])
def list_service_records(
    skip: int = 0,
    limit: int = 100,
    vehicle_id: int = Query(None),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    query = db.query(models.ServiceRecord).filter(
        models.ServiceRecord.user_id == current_user.id
    )
    
    if vehicle_id:
        query = query.filter(models.ServiceRecord.vehicle_id == vehicle_id)
    
    services = query.order_by(
        models.ServiceRecord.service_date.desc()
    ).offset(skip).limit(limit).all()
    
    return services

@router.get("/{service_id}", response_model=schemas.ServiceRecordResponse)
def get_service_record(
    service_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    service = db.query(models.ServiceRecord).filter(
        models.ServiceRecord.id == service_id,
        models.ServiceRecord.user_id == current_user.id
    ).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service record not found")
    return service

@router.delete("/{service_id}")
def delete_service_record(
    service_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    service = db.query(models.ServiceRecord).filter(
        models.ServiceRecord.id == service_id,
        models.ServiceRecord.user_id == current_user.id
    ).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service record not found")
    
    db.delete(service)
    db.commit()
    return {"message": "Service record deleted successfully"}
