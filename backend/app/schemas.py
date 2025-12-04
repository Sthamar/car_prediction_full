from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=72)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Prediction models
class CarData(BaseModel):
    make: str
    model: str
    year: int
    mileage: float
    last_service_date: str
    engine_size: float
    transmission: str
    fuel_type: str

class PredictionResponse(BaseModel):
    service_needed: bool
    confidence: float
    estimated_days_until_service: int
    recommended_services: List[str]
    risk_level: str

# Vehicle schemas
class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    vin: Optional[str] = None
    nickname: Optional[str] = None
    mileage: float = 0.0
    engine_size: Optional[float] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    is_default: bool = False

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vin: Optional[str] = None
    nickname: Optional[str] = None
    mileage: Optional[float] = None
    engine_size: Optional[float] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    is_default: Optional[bool] = None

class VehicleResponse(VehicleBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Prediction History schemas
class PredictionHistoryCreate(BaseModel):
    vehicle_id: Optional[int] = None
    make: str
    model: str
    year: int
    mileage: float
    last_service_date: Optional[str] = None
    engine_size: Optional[float] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    service_needed: bool
    confidence: float
    estimated_days_until_service: int
    recommended_services: str  # JSON string
    risk_level: str

class PredictionHistoryResponse(BaseModel):
    id: int
    user_id: int
    vehicle_id: Optional[int]
    make: str
    model: str
    year: int
    mileage: float
    service_needed: bool
    confidence: float
    estimated_days_until_service: int
    recommended_services: str
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True

# Service Record schemas
class ServiceRecordCreate(BaseModel):
    vehicle_id: Optional[int] = None
    service_type: str
    service_date: datetime
    cost: Optional[float] = None
    mileage_at_service: Optional[float] = None
    notes: Optional[str] = None

class ServiceRecordResponse(BaseModel):
    id: int
    user_id: int
    vehicle_id: Optional[int]
    service_type: str
    service_date: datetime
    cost: Optional[float]
    mileage_at_service: Optional[float]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Statistics schema
class UserStatistics(BaseModel):
    total_predictions: int
    total_vehicles: int
    total_services: int
    predictions_this_month: int
    upcoming_services: int

# Vehicle Catalog schemas
class VehicleMakeBase(BaseModel):
    name: str

class VehicleMakeCreate(VehicleMakeBase):
    pass

class VehicleMakeResponse(VehicleMakeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VehicleModelBase(BaseModel):
    name: str
    make_id: int

class VehicleModelCreate(VehicleModelBase):
    pass

class VehicleModelResponse(VehicleModelBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VehicleMakeWithModels(VehicleMakeResponse):
    models: List['VehicleModelResponse'] = []

    class Config:
        from_attributes = True
