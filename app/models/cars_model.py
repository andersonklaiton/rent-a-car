from dataclasses import dataclass
from email.policy import default
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from datetime import date

from app.configs.database import db

@dataclass
class Cars(db.Model):
    chassis: str
    license_plate: str
    brand: str
    model: str
    year: str
    car_color: str
    image: str
    current_km: float
    licensing_expiration: date
    daily_rental_price: float
    daily_fix_km: int
    available: bool
    category_id: int
    maintenance_id: int

    __tablename__ = 'tb_cars'

    chassis = Column(String, primary_key = True)
    license_plate = Column(String(7), unique = True, nullable = False)
    brand = Column(String, nullable = False)
    model = Column(String, nullable = False)
    year = Column(String, nullable = False)
    car_color = Column(String, nullable = False)
    image = Column(String, nullable = False)
    current_km = Column(Float, nullable = False)
    licensing_expiration = Column(DateTime, nullable = False)
    daily_rental_price = Column(Float, nullable = False)
    daily_fix_km = Column(Integer, nullable = False)
    available = Column(Boolean, default = True)

    category_id = Column(Integer, ForeignKey('tb_category_car.category_id'), nullable = False)
    maintenance_id = Column(Integer, ForeignKey('tb_maintenance_car.maintenance_id'))