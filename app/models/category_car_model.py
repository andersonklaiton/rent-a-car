from dataclasses import dataclass
from sqlalchemy import Column, Float, String, Integer
from app.configs.database import db
from sqlalchemy.orm import relationship, backref

@dataclass
class Category_car(db.Model):
    keys = ['body_types', 'fuel_type', 'engine_power', 'km_per_liter', 'allowed_category_cnh', 'differentials']

    category_id: int
    body_types: str
    fuel_type: str
    engine_power: str
    km_per_liter: float
    allowed_category_cnh: str
    differentials: str

    __tablename__ = 'tb_category_car'

    category_id = Column(Integer, primary_key = True)
    body_types = Column(String, nullable = False)
    fuel_type = Column(String, nullable = False)
    engine_power = Column(String, nullable = False)
    km_per_liter = Column(Float, nullable = False)
    allowed_category_cnh = Column(String(2), nullable = False)
    differentials = Column(String, nullable = False)

    cars = relationship('Cars', backref=backref('category'), uselist = False)