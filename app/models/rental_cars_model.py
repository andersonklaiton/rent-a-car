from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from datetime import date

from app.configs.database import db

@dataclass
class RentalCars(db.Model):
    create_keys = ['rental_date', 'rental_return_date', 'customer_cnh', 'car_license_plate', 'rental_total_days']
    return_keys = ['rental_real_return_date', 'rental_real_total_days', 'total_returned_km', 'cnh', 'car_license_plate']

    rental_id: int
    rental_date: date
    rental_return_date: date
    rental_real_return_date: date
    returned_car: bool
    rental_total_days: int
    initial_km: float
    final_km: float
    total_fixed_km: int
    total_returned_km: float
    rental_value: float
    rental_real_value: float
    customer_cnh: str
    car_licence_plate: str

    __tablename__ = 'tb_rental_cars'

    rental_id = Column(Integer, primary_key=True)
    rental_date = Column(DateTime, nullable=False)
    rental_return_date = Column(DateTime, nullable=False)
    rental_real_return_date = Column(DateTime)
    returned_car = Column(Boolean)
    rental_total_days = Column(Integer, nullable=False)
    rental_real_total_days = Column(Integer)
    initial_km = Column(Float, nullable=False)
    final_km = Column(Float)
    total_fixed_km = Column(Integer, nullable=False)
    total_returned_km = Column(Float)
    rental_value = Column(Float, nullable=False)
    rental_real_value = Column(Float)
    customer_cnh = Column(String, ForeignKey('tb_users.cnh') ,nullable=False)
    car_license_plate = Column(String, ForeignKey('tb_cars.license_plate') ,nullable=False)
