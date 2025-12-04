from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import auth, models, schemas

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.post("/", response_model=schemas.VehicleResponse)
def create_vehicle(
    vehicle: schemas.VehicleCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    # If this is set as default, unset other defaults
    if vehicle.is_default:
        db.query(models.Vehicle).filter(
            models.Vehicle.user_id == current_user.id,
            models.Vehicle.is_default == True
        ).update({"is_default": False})
    
    db_vehicle = models.Vehicle(**vehicle.dict(), user_id=current_user.id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("/", response_model=List[schemas.VehicleResponse])
def list_vehicles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    vehicles = db.query(models.Vehicle).filter(
        models.Vehicle.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return vehicles

@router.get("/{vehicle_id}", response_model=schemas.VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id,
        models.Vehicle.user_id == current_user.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.put("/{vehicle_id}", response_model=schemas.VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_update: schemas.VehicleUpdate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    db_vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id,
        models.Vehicle.user_id == current_user.id
    ).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    # If setting as default, unset other defaults
    if vehicle_update.is_default:
        db.query(models.Vehicle).filter(
            models.Vehicle.user_id == current_user.id,
            models.Vehicle.id != vehicle_id,
            models.Vehicle.is_default == True
        ).update({"is_default": False})
    
    update_data = vehicle_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == vehicle_id,
        models.Vehicle.user_id == current_user.id
    ).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}
