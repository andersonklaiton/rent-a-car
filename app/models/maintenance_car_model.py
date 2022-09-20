from dataclasses import dataclass
from array import array
from sqlalchemy import Column, Integer, DateTime, Float, String
from datetime import date

from app.configs.database import db

@dataclass
class Maintenance(db.Model):
    keys = ['last_maintenance', 'next_maintenance', 'repaired_items', 'maintenance_price', 'car_license_plate']

    maintenance_id: int
    last_maintenance: date
    next_maintenance: date
    repaired_items: str
    maintenance_price: float
    car_license_plate: str

    __tablename__ = 'tb_maintenance_car'

    maintenance_id = Column(Integer, primary_key = True)
    last_maintenance = Column(DateTime, nullable = False)
    next_maintenance = Column(DateTime, nullable = False)
    repaired_items = Column(db.ARRAY(String), nullable = False)
    maintenance_price = Column(Float, nullable = False)
    car_license_plate = Column(String, nullable = False)

    @staticmethod
    def format_date(date):
        format = date.strftime("%d/%m/%Y")
        return format