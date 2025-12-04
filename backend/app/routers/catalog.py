from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import auth, models, schemas

router = APIRouter(prefix="/catalog", tags=["catalog"])

# Public endpoints - anyone can view the catalog
@router.get("/makes", response_model=List[schemas.VehicleMakeWithModels])
def list_makes(
    db: Session = Depends(auth.get_db),
):
    makes = db.query(models.VehicleMake).all()
    return makes

@router.get("/makes/{make_id}/models", response_model=List[schemas.VehicleModelResponse])
def list_models_for_make(
    make_id: int,
    db: Session = Depends(auth.get_db),
):
    models_list = db.query(models.VehicleModel).filter(
        models.VehicleModel.make_id == make_id
    ).all()
    return models_list

# Admin-only endpoints
@router.post("/makes", response_model=schemas.VehicleMakeResponse)
def create_make(
    make: schemas.VehicleMakeCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_superuser),
):
    # Check if make already exists
    existing = db.query(models.VehicleMake).filter(
        models.VehicleMake.name == make.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Make already exists")
    
    db_make = models.VehicleMake(**make.dict())
    db.add(db_make)
    db.commit()
    db.refresh(db_make)
    return db_make

@router.post("/models", response_model=schemas.VehicleModelResponse)
def create_model(
    model: schemas.VehicleModelCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_superuser),
):
    # Check if make exists
    make = db.query(models.VehicleMake).filter(
        models.VehicleMake.id == model.make_id
    ).first()
    if not make:
        raise HTTPException(status_code=404, detail="Make not found")
    
    # Check if model already exists for this make
    existing = db.query(models.VehicleModel).filter(
        models.VehicleModel.make_id == model.make_id,
        models.VehicleModel.name == model.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Model already exists for this make")
    
    db_model = models.VehicleModel(**model.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.delete("/makes/{make_id}")
def delete_make(
    make_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_superuser),
):
    make = db.query(models.VehicleMake).filter(
        models.VehicleMake.id == make_id
    ).first()
    if not make:
        raise HTTPException(status_code=404, detail="Make not found")
    
    db.delete(make)
    db.commit()
    return {"message": "Make deleted successfully"}

@router.delete("/models/{model_id}")
def delete_model(
    model_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_superuser),
):
    model = db.query(models.VehicleModel).filter(
        models.VehicleModel.id == model_id
    ).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db.delete(model)
    db.commit()
    return {"message": "Model deleted successfully"}
