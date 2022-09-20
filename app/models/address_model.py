from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.configs.database import db

@dataclass
class Address(db.Model):
    address_id: int
    street: str
    number: str
    district: str
    zip_code: str
    city: str
    reference: str
    state_id: int

    __tablename__ = 'tb_address'

    address_id = Column(Integer, primary_key = True)
    street = Column(String, nullable = False)
    number = Column(String, nullable = False)
    district = Column(String, nullable = False)
    zip_code = Column(String(8), nullable = False)
    city = Column(String, nullable = False)
    reference = Column(String, nullable = False)
    state_id = Column(Integer, ForeignKey('tb_states.state_id'), nullable = False)
    address = relationship("Users", back_populates='user_address', uselist=False)