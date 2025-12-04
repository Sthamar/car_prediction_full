from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    predictions = relationship("PredictionHistory", back_populates="user", cascade="all, delete-orphan")
    services = relationship("ServiceRecord", back_populates="user", cascade="all, delete-orphan")


class VehicleMake(Base):
    __tablename__ = "vehicle_makes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    models = relationship("VehicleModel", back_populates="make", cascade="all, delete-orphan")


class VehicleModel(Base):
    __tablename__ = "vehicle_models"

    id = Column(Integer, primary_key=True, index=True)
    make_id = Column(Integer, ForeignKey("vehicle_makes.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    make = relationship("VehicleMake", back_populates="models")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    vin = Column(String, unique=True, nullable=True)
    nickname = Column(String, nullable=True)
    mileage = Column(Float, default=0.0)
    engine_size = Column(Float, nullable=True)
    transmission = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="vehicles")
    predictions = relationship("PredictionHistory", back_populates="vehicle", cascade="all, delete-orphan")
    services = relationship("ServiceRecord", back_populates="vehicle", cascade="all, delete-orphan")


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    
    # Car details at time of prediction
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    mileage = Column(Float)
    last_service_date = Column(String, nullable=True)
    engine_size = Column(Float, nullable=True)
    transmission = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)
    
    # Prediction results
    service_needed = Column(Boolean)
    confidence = Column(Float)
    estimated_days_until_service = Column(Integer)
    recommended_services = Column(Text)  # JSON string
    risk_level = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    vehicle = relationship("Vehicle", back_populates="predictions")


class ServiceRecord(Base):
    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    
    service_type = Column(String, nullable=False)
    service_date = Column(DateTime, nullable=False)
    cost = Column(Float, nullable=True)
    mileage_at_service = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="services")
    vehicle = relationship("Vehicle", back_populates="services")
